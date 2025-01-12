#include "bspline.h"
#include <cassert>

BSpline::BSpline(int order, double resolution, double xmin, double xmax)
{
    extrapolation = TRUNC;

    this->order = order;
    this->resolution = resolution;
    this->xmin = xmin;
    this->xmax = xmax;

    nbreak = get_nbreak(xmin, xmax, resolution);
    ncoeff = order + nbreak - 2;
    //printf("BSPLINE: %d %lf %lf %lf %d %d\n", order, resolution, xmin, xmax, nbreak, ncoeff);

    bw = gsl_bspline_alloc(order, nbreak);
    gsl_bspline_knots_uniform(xmin, xmax, bw);

    B = gsl_vector_calloc(order);
    D = gsl_vector_calloc(order);

    table_bvalue = 0;
    table_istart = 0;
    table_nn = 0;
    ddx = 0.0;

    m = gsl_matrix_alloc(order, 2);
    mt = gsl_matrix_alloc(2, order);

    D0 = gsl_vector_calloc(order);
    D1 = gsl_vector_calloc(order);

    size_t iend;

    B0 = gsl_vector_calloc(order);
    D0 = gsl_vector_calloc(order);
    gsl_bspline_eval_nonzero(xmin, B0, &start0, &iend, bw);
    gsl_bspline_deriv_eval_nonzero(xmin, 1, m, &start0, &iend, bw);
    gsl_matrix_transpose_memcpy(mt, m);
    gsl_matrix_get_row(D0, mt, 1);

    B1 = gsl_vector_calloc(order);
    D1 = gsl_vector_calloc(order);
    gsl_bspline_eval_nonzero(xmax, B1, &start1, &iend, bw);
    gsl_bspline_deriv_eval_nonzero(xmax, 1, m, &start1, &iend, bw);
    gsl_matrix_transpose_memcpy(mt, m);
    gsl_matrix_get_row(D1, mt, 1);
}

BSpline::~BSpline()
{
    gsl_bspline_free(bw);
    gsl_vector_free(B);
    gsl_vector_free(D);
    gsl_vector_free(D0);
    gsl_vector_free(B0);
    gsl_vector_free(D1);
    gsl_vector_free(B1);
    gsl_matrix_free(m);
    gsl_matrix_free(mt);

    if(table_bvalue)
    {
        delete [] table_bvalue;
        delete [] table_istart;
        delete [] table_nn;
    }
}

void BSpline::setup_cache(double dx_factor)
{
    ddx = dx_factor * resolution;
    int tsize = static_cast<int>(round((xmax - xmin) / ddx)) + 1;
    table_bvalue = new double [tsize * order];
    table_istart = new int [tsize];
    table_nn = new int [tsize];

    for(size_t i=0; i<tsize; i++)
    {
        size_t istart, iend;
        double dx = xmin + (i==0?SMALL:ddx*i);
        if(dx>=xmax) dx = xmax - SMALL;

        gsl_bspline_eval_nonzero(dx, B, &istart, &iend, bw);

        int nn = iend - istart + 1;
        table_istart[i] = istart;
        table_nn[i] = nn;

        for(int j=0; j<nn; j++) table_bvalue[i*order+j] = B->data[j];
    }
}

void BSpline::eval_coeffs(double x, double **b, size_t *istart, int *nn)
{
    if(extrapolation == CAP && x<=xmin) x = xmin + SMALL;
    else if(extrapolation == CAP && x>=xmax) x = xmax - SMALL;

    if(x<=xmin)
    {
        if(extrapolation == TRUNC) gsl_vector_set_zero(B);
        else
        {
            gsl_vector_memcpy(B, D0);
            gsl_vector_scale(B, (x-xmin));
            gsl_vector_add(B, B0);
        }

        (*istart) = start0;
        (*nn) = order;
        (*b) = B->data;
    }
    else if(x>=xmax)
    {
        if(extrapolation == TRUNC) gsl_vector_set_zero(B);
        else
        {
            gsl_vector_memcpy(B, D1);
            gsl_vector_scale(B, (x-xmax));
            gsl_vector_add(B, B1);
        }

        (*istart) = start1;
        (*nn) = order;
        (*b) = B->data;
    }
    else if(table_bvalue)
    {
        int it = static_cast<int>(round((x - xmin) / ddx));
        (*b) = table_bvalue + it * order;
        (*istart) = table_istart[it];
        (*nn) = table_nn[it];
    }
    else
    {
        size_t iend;
        gsl_bspline_eval_nonzero(x, B, istart, &iend, bw);
        (*nn) = iend - (*istart) + 1;
        (*b) = B->data;
    }
}

void BSpline::eval_derivs(double x, double **b, size_t *istart, int *nn)
{
    /*--- current limitations:
    Because only the 3-body NB term need evaluations of derivatives at the
    moment, so this function is not optmized with cache. Will consider to
    add it later as what was done in eval().
    */

    if(extrapolation == CAP && x<=xmin) x = xmin + SMALL;
    else if(extrapolation == CAP && x>=xmax) x = xmax - SMALL;

    if(x<=xmin)
    {
        if(extrapolation == TRUNC) gsl_vector_set_zero(D);
        else
        {
            assert(0 && "Linear extrapolation method is not supported yet");
        }

        (*istart) = start0;
        (*nn) = order;
        (*b) = D->data;
    }
    else if(x>=xmax)
    {
        if(extrapolation == TRUNC) gsl_vector_set_zero(D);
        else
        {
            assert(0 && "Linear extrapolation method is not supported yet");
        }

        (*istart) = start1;
        (*nn) = order;
        (*b) = D->data;
    }
    else if(0 /* table_bvalue */)
    {

    }
    else
    {
        size_t iend;
        gsl_bspline_deriv_eval_nonzero(x, 1, m, istart, &iend, bw);
        gsl_matrix_transpose_memcpy(mt, m);
        gsl_matrix_get_row(D, mt, 1);

        (*nn) = iend - (*istart) + 1;
        (*b) = D->data;
    }
}

void BSpline::eval(double *input, double *output, double xmin, double dx, int n)
{
    gsl_vector *Bs = gsl_vector_calloc(ncoeff);
    gsl_vector *Cs = gsl_vector_calloc(ncoeff);

    for(int i=0; i<ncoeff; i++) gsl_vector_set(Cs, i, input[i]);

    for(int i=0; i<n; i++)
    {
        size_t istart;
        int nn;
        double *b;

        double x = xmin + dx * i;
        eval_coeffs(x, &b, &istart, &nn);

        gsl_vector_set_zero(Bs);
        for(int c=0; c<nn; c++) Bs->data[istart+c] = b[c];
        gsl_blas_ddot(Bs, Cs, output++);
    }

    gsl_vector_free(Bs);
    gsl_vector_free(Cs);
}

void BSpline::eval(double *knots, double *in, double *out, int size)
{
    ExtrapolationMethod save = extrapolation;
    extrapolation = LINEAR;

    gsl_vector *Bs = gsl_vector_calloc(ncoeff);
    gsl_vector *Cs = gsl_vector_calloc(ncoeff);

    for(int i=0; i<ncoeff; i++) gsl_vector_set(Cs, i, knots[i]);

    for(int i=0; i<size; i++)
    {
        size_t istart;
        int nn;
        double *b;

        double x = in[i];
        eval_coeffs(x, &b, &istart, &nn);

        gsl_vector_set_zero(Bs);
        for(int c=0; c<nn; c++) Bs->data[istart+c] = b[c];
        gsl_blas_ddot(Bs, Cs, out++);
    }

    gsl_vector_free(Bs);
    gsl_vector_free(Cs);

    extrapolation = save;
}

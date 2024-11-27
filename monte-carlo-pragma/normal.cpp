#include <iostream>
#include <bitset>
#include <omp.h>
#include <stdio.h>

#include <random>
#include <cstdlib>
#include <ctime>
#include <climits>

using namespace std;

double dist(double koord_x, double koord_y, double koord_z) {
    return abs(koord_x) + abs(koord_y) + abs(koord_z);
}
double random_xorshift(double min, double max,double result) {
    double random = (double) (result) / UINT_MAX;
    return min + random * (max - min);
}
double dist_between_two_points(double octahedronX1, double octahedronY1, double octahedronZ1, double octahedronX2, double octahedronY2, double octahedronZ2) {
    return sqrt(pow(octahedronX2 - octahedronX1, 2) + pow(octahedronY1 - octahedronY2, 2)+pow(octahedronZ1-octahedronZ2,2));
}
int parse_int(char* s)
{
    bool negate = (s[0] == '-');
    if (*s == '+' || *s == '-')
        ++s;
    int result = 0;
    while (*s)
    {
        result = result * 10 - (*s - '0');
        ++s;
    }
    return negate ? result : -result;
}

int main(int args, char* argv[]) {
    char* program_name = argv[0];
    int omp_num=14;
    double result;
    omp_num = parse_int(argv[1]);
    int generator;
    time_t t1 = time(NULL);
    unsigned int number = (unsigned int) (t1);
    if (args == 5) {
        generator = parse_int(argv[4]);
    }
    else {
        generator = 1;
    }
    long long count_of_point;
    char* file_in = argv[2];
    char* file_out = argv[3];
    double octahedronX1, octahedronY1, octahedronZ1;
    double octahedronX2, octahedronY2, octahedronZ2;
    double octahedronX3, octahedronY3, octahedronZ3;

    FILE * fin = fopen(file_in, "r");
    fscanf(fin, "%lli\n(%la %la %la)\n(%la %la %la)\n(%la %la %la)\n", 
                        &count_of_point, &octahedronX1, &octahedronY1, &octahedronZ1, 
                        &octahedronX2, &octahedronY2, &octahedronZ2,
                        &octahedronX3, &octahedronY3, &octahedronZ3);
    fclose(fin);
    double len_of_storon = min(min(dist_between_two_points(octahedronX1, octahedronY1,octahedronZ1,octahedronX2,octahedronY2, octahedronZ2),dist_between_two_points(octahedronX2, octahedronY2, octahedronZ2, octahedronX3, octahedronY3, octahedronZ3)),dist_between_two_points(octahedronX1, octahedronY1, octahedronZ1, octahedronX3, octahedronY3, octahedronZ3));
    double length_square=len_of_storon * pow(2,0.5);
    double objem = pow(len_of_storon,3) * pow(2,0.5) / 3;
    double area = pow(length_square,3);
    double length_okr = length_square / 2;
    double octahedronCenterX = 0;
    double octahedronCenterY = 0;
    double octahedronCenterZ = 0;
    double start = omp_get_wtime();

    if (generator == 0) {
        long long count_in = 0;  
        #pragma omp parallel if(omp_num > 0) num_threads(omp_num)
        {
            long long local_in = 0;
            double point_x;
            double point_y;
            double point_z;

            mt19937 gen(10 + 15 * omp_get_thread_num());
            
            #pragma omp for schedule(static)
            for (long long i = 0; i < count_of_point; i++) {
                //cout >> i;
                point_x = (double)gen() / UINT_MAX * (length_square)-length_okr;
                point_y = (double)gen() / UINT_MAX * (length_square)-length_okr;
                point_z = (double)gen() / UINT_MAX * (length_square)-length_okr;
                if (dist(point_x, point_y, point_z) <= length_okr) {
                    local_in += 1;
                }
            }
            #pragma omp atomic
            count_in += local_in;
        }
        result = (double) count_in / count_of_point;
        result *= (double) area;
        //cout << result << '\n';
    } else if (generator == 1) {
        long long count_in = 0;
        #pragma omp parallel if(omp_num > 0) num_threads(omp_num)
        {
            long long local_in = 0;
            
            unsigned int t;
            unsigned int p = number* 4968205778;
            unsigned int r = 8287104867*number;
            unsigned int s = 6928571081*number;
            unsigned int u = 4562396734 * number;
            double point_x;
            double point_y;
            double point_z;            
            #pragma omp for schedule(static)
            for (long long i = 0; i < count_of_point; i++) {
                t = p ^ (p << 11);
                p = r;
                r = s;
                s = u;
                double point_x =double(u) / UINT_MAX * (length_square)-length_okr;
                u = u ^ (u >> 19) ^ t ^ (t >> 8);

                t = p ^ (p << 11);
                p = r;
                r = s;
                s = u;
                double point_y = double(u) / UINT_MAX * (length_square)-length_okr;
                u = u ^ (u >> 19) ^ t ^ (t >> 8);

                t = p ^ (p << 11);
                p = r;
                r = s;
                s = u;
                double point_z = double(u) / UINT_MAX * (length_square)-length_okr;
                u = u ^ (u >> 19) ^ t ^ (t >> 8);
                if (dist(point_x, point_y, point_z) <= length_okr) {
                    local_in += 1;
                }
            }
            #pragma omp atomic
            count_in += local_in;
        }
        result = (double) count_in / count_of_point;
        result *= area;
    } else if (generator == 2) {
        long long count_in = 0;
        #pragma omp parallel if(omp_num > 0) num_threads(omp_num)
        {
            srand(time(NULL));
            long long local_in = 0;
            double point_x;
            double point_y;
            double point_z;
            #pragma omp for schedule(static)
            for (long long i = 0; i < count_of_point; i++) {
                point_x = (double)rand() / RAND_MAX * (length_square) - length_okr;        
                point_y = (double)rand() / RAND_MAX * (length_square) - length_okr;
                point_z = (double)rand() / RAND_MAX * (length_square) - length_okr;
                if (dist(point_x, point_y, point_z) <= length_okr) {
                    local_in += 1;
                }
            }
            #pragma omp atomic
            count_in += local_in;
        }
        result = (double) count_in / count_of_point;
        result *= area;
    }
    FILE *fcl = fopen(file_out, "w");
    fprintf(fcl,"%g ",objem);
    fprintf(fcl,"%g\n",result);
    fclose(fcl);
    double end = omp_get_wtime();
    cout << (end - start);
}




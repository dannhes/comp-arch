#include <iostream>
#include <bitset>
#include <omp.h>
#include <stdio.h>
#include <random>
#include <cstdlib>
#include <ctime>
#include <climits>

using namespace std;

int xorshift32(unsigned int seed) {
    seed ^= seed << 13;
    seed ^= seed >> 17;
    seed ^= seed << 5;
    return seed;
}
double dist(double koord_x, double koord_y, double koord_z) {
    return abs(koord_x) + abs(koord_y) + abs(koord_z);
}
double random_xorshift(double min, double max, unsigned int seed) {
    double random = (double) (xorshift32(seed)) / UINT_MAX;
    return min + random * (max - min);
}
double dist_between_two_points(double octahedronX1, double octahedronY1, double octahedronZ1, double octahedronX2, double octahedronY2, double octahedronZ2) {
    return sqrt(pow(octahedronX2 - octahedronX1, 2) + pow(octahedronY1 - octahedronY2, 2)+pow(octahedronZ1-octahedronZ2,2));
}
double random_rand(double min, double max) {
    return min + (double) rand() / RAND_MAX * (max - min);
}
int parse_int(char* number) {
    int value = 0, sign = 1;
    if (*number == '-') {
        sign = -1;
        number++;
    }
    while (*number) {
        value *= 10;
        value += (*number) - '0';
        number++;
    }
    return value * sign;
}
int main(int args, char* argv[]) {
    char* program_name = argv[0];
    int omp_num = parse_int(argv[1]);
    int generator;
    if (args == 5) {
        generator = parse_int(argv[4]);
    }
    else {
        generator = 0;
    }
    long long count_of_point;
    char* file_in = argv[2];
    char* file_out = argv[3];
    // cout << omp_num;
    // cout << program_name << ' ' << omp_num << ' ' << file_in << ' ' << file_out << ' ' << generator;
    // return 0;
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
    double length_okr = length_square / 2;
    double octahedronCenterX = 0;
    double octahedronCenterY = 0;
    double octahedronCenterZ = 0;

    double start = omp_get_wtime();

    if (generator == 0) {
        long long count_in = 0;  
        #pragma omp parallel num_threads(omp_num)
        {
            long long local_in = 0;
            double point_x;
            double point_y;
            double point_z;

            mt19937 gen(10 + 15 * omp_get_thread_num());
            
            #pragma omp for
            for (long long i = 0; i < count_of_point; i++) {
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
        double result = (double) count_in / count_of_point;
        cout << result << '\n';
    } else if (generator == 1) {
        long long count_in = 0;
        unsigned int seed = 12345; // Начальное значение семени
        #pragma omp parallel num_threads(omp_num)
        {
            long long local_in = 0;
            double point_x;
            double point_y;
            double point_z;
            
            #pragma omp for
            for (long long i = 0; i < count_of_point; i++) {
                point_x = random_xorshift(length_square * (-1), length_square, seed);
                point_y = random_xorshift(length_square * (-1), length_square, seed);
                point_z = random_xorshift(length_square * (-1), length_square, seed);
                if (dist(point_x, point_y, point_z) <= length_okr) {
                    local_in += 1;
                }
            }
            #pragma omp atomic
            count_in += local_in;
        }
        double result = (double) count_in / count_of_point;
        cout << result << '\n';
    } else if (generator == 2) {
        srand((time(nullptr))); // Инициализируем генератор случайных чисел
        long long count_in = 0;
        #pragma omp parallel num_threads(omp_num)
        {
            long long local_in = 0;
            double point_x;
            double point_y;
            double point_z;
            #pragma omp for
            for (long long i = 0; i < count_of_point; i++) {
                point_x = random_rand(length_square * (-1), length_square);
                point_y = random_rand(length_square * (-1), length_square);
                point_z = random_rand(length_square * (-1), length_square);
                if (dist(point_x, point_y, point_z) <= length_okr) {
                    local_in += 1;
                }
            }
            #pragma omp atomic
            count_in += local_in;
        }
        double result = (double) count_in / count_of_point;
        cout << result << '\n';
    }

    double end = omp_get_wtime();
    cout << end - start;
}



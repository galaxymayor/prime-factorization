#include"prime16.c"
#include<stdlib.h>

typedef struct Pow{
    int base, exp;
} Pow;

typedef struct Factors{
    unsigned int i, factors_count;
    Pow *factors;
} Factors;

Factors decompose(unsigned int i){
    unsigned num = i;
    unsigned capacity = 4, size=0;
    Pow *fs = calloc(4, sizeof(Factors));

    for(unsigned p=0; PRIME16[p]*PRIME16[p]<=i&&p<5642; ++p){
        if(i % PRIME16[p]){
            continue;
        }

        if(size==capacity){
            capacity<<=1;
            realloc(fs, capacity);
        }
        fs[size++] = (Pow){PRIME16[p], 0};

        do{
            i/=PRIME16[p];
            fs[size-1].exp++;
        }while(!(i%PRIME16[p]));
    }

    if(i!=1){
        if(size==capacity){
            capacity<<=1;
            realloc(fs, capacity);
        }
        fs[size++] = (Pow){i, 1};
    }


    return (Factors){num, size, fs};
}

void free_factors(Factors f){
    free(f.factors);
}

void free_ptr(void *_Memory){
    free(_Memory);
}
//test 

// #include<stdio.h>
// int main(){
//     Factors f;
//     for(unsigned i=4293001441; i<4293001500; ++i){
//         f = decompose(i);
//         printf("decompose %u: ", i);
//         for(int j=0; j<f.factors_count; ++j){
//             printf("(%u, %u)", f.factors[j].base, f.factors[j].exp);
//         }
//         puts("");
//         free(f.factors);
//     }
// }

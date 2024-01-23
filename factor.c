#include"prime16.c"
#include<stdlib.h>

#define ull unsigned long long
typedef struct Pow{
    ull base;
    short exp;
} Pow;

typedef struct Factors{
    ull i;
    unsigned factors_count;
    Pow *factors;
} Factors;

Factors decompose(ull i){ //  i < 2^50
    Factors ans = {i, .factors=malloc(4*sizeof(Pow))};
    unsigned size=0;
    unsigned capacity = 4;

    ull p;
    for(int o=0; o<6542 && (p = PRIME16[o], p*p<=i); ++o){
        if(i % p){
            continue;
        }

        if(size == capacity){
            capacity += 3;
            ans.factors = realloc(ans.factors, capacity*sizeof(Pow));
        }
        ans.factors[size++] = (Pow){p, 0};

        do{
            i/=p;
            ans.factors[size-1].exp++;
        }while(!(i%p));
    }

    if(i==1){
        ans.factors_count = size;
        return ans;
    }

    if(i<0x100000000){
        if(size == capacity){
            ans.factors = realloc(ans.factors, (++capacity)*sizeof(Pow));
        }
        ans.factors[size++] = (Pow){i, 1};
        ans.factors_count = size;
        return ans;
    }

    ull test = 65537;

    do{
        if(!(i%test)){
            if(size == capacity){
                capacity += 2;
                ans.factors = realloc(ans.factors, capacity*sizeof(Pow));
            }
            ans.factors[size++] = (Pow){test, 0};
            do{
                i/=test;
                ans.factors[size-1].exp++;
            }while(!(i%test));
        }
        test+=2;
        if(!(i%test)){
            if(size == capacity){
                capacity += 2;
                ans.factors = realloc(ans.factors, capacity*sizeof(Pow));
            }
            ans.factors[size++] = (Pow){test, 0};
            do{
                i/=test;
                ans.factors[size-1].exp++;
            }while(!(i%test));
        }
        test+=4;
    }while(test<33554432&&test*test<=i); // 2^25

    if(i==1){
        ans.factors_count = size;
        return ans;
    }

    if(size == capacity){
        ans.factors = realloc(ans.factors, (++capacity)*sizeof(Pow));
    }
    ans.factors[size++] = (Pow){i, 1};
    ans.factors_count = size;
    return ans;
}

void free_ptr(void *_Memory){
    free(_Memory);
}
//test 

// #include<stdio.h>
// int main(){
//     Factors f;
//     for(ull i=1; i<100; ++i){
//         f = decompose(i);
//         printf("decompose %llu: ", i);
//         for(int j=0; j<f.factors_count; ++j){
//             printf("(%llu, %llu)", f.factors[j].base, f.factors[j].exp);
//         }
//         puts("");
//         free(f.factors);
//     }
// }

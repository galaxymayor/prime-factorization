#include<stdio.h>
#define P16 PRIME16
#define S16(i) (P16[i]*P16[i])

unsigned short PRIME16[6542];


int main(){
    FILE *f1p = fopen(".\\prime16.enum16", "rb");
    fread(PRIME16, sizeof(short), 6542, f1p);
    fclose(f1p);

    FILE *f2p = fopen(".\\prime16.c", "w");
    fputs("unsigned short PRIME16[6542] = {\n" , f2p);

    for(int i=0; i<6536; i+=8){
        fprintf(
            f2p, "    %hu, %hu, %hu, %hu, %hu, %hu, %hu, %hu,\n",
            P16[i], P16[i+1], P16[i+2], P16[i+3], P16[i+4], P16[i+5], P16[i+6], P16[i+7]);
    }

    fprintf(f2p, "    %hu, %hu, %hu, %hu, %hu, %hu\n};\n",
            P16[6536], P16[6537], P16[6538], P16[6539], P16[6540], P16[6541]);


    fputs("\n\nunsigned int SQ_PRIME16[6542] = {\n" , f2p);

    for(int i=0; i<6536; i+=8){
        fprintf(
            f2p, "    %u, %u, %u, %u, %u, %u, %u, %u,\n",
            S16(i), S16(i+1), S16(i+2), S16(i+3), S16(i+4), S16(i+5), S16(i+6), S16(i+7));
    }

    fprintf(f2p, "    %u, %u, %u, %u, %u, %u\n};\n",
            S16(6536), S16(6537), S16(6538), S16(6539), S16(6540), S16(6541));
    
    fclose(f2p);
}

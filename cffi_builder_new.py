from cffi import FFI
ffibuilder = FFI()

ffibuilder.cdef("""
typedef struct Pow{
    unsigned long long base;
    short exp;
} Pow;

typedef struct Factors{
    unsigned long long i;
    unsigned factors_count;
    Pow *factors;
} Factors;

extern size_t new(size_t i, unsigned size, size_t factors);
extern size_t copy(size_t f);
extern size_t mul(size_t a, size_t b);
extern size_t _pow(size_t f, unsigned exp);
extern void _ipow(size_t fp, unsigned exp);
extern size_t gcd(size_t a, size_t b);
extern size_t decompose_u32(unsigned i);
extern size_t decompose(size_t i);
extern unsigned short int* get_prime16_p();
extern unsigned int* get_sq_prime16_p();
extern void free_ptr(void *_Memory);
extern void free_address(size_t _Memory);
extern void free_facted(size_t fp);
 """)

# set_source() gives the name of the python extension module to
# produce, and some C source code as a string. This C code needs
# to make the declarated functions, types and globals available,
# so it is often just the "#include".
ffibuilder.set_source("fact_c_new",
"""
typedef struct Pow{
    unsigned long long base;
    short exp;
} Pow;

typedef struct Factors{
    unsigned long long i;
    unsigned factors_count;
    Pow *factors;
} Factors;

size_t new(size_t i, unsigned size, size_t factors);
size_t copy(size_t f);
size_t mul(size_t a, size_t b);
size_t _pow(size_t f, unsigned exp);
void _ipow(size_t fp, unsigned exp);
size_t gcd(size_t a, size_t b);
size_t decompose_u32(unsigned i);
size_t decompose(size_t i);
unsigned short int* get_prime16_p();
unsigned int* get_sq_prime16_p();
void free_ptr(void *_Memory);
void free_address(size_t _Memory);
void free_facted(size_t fp);
""",
    sources = ['new_fact.c'],
    library_dirs = [],
    libraries = [],
    extra_compile_args=["-O2"]
)

if __name__ == '__main__':
    ffibuilder.compile(verbose=True)

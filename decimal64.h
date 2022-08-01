
#pragma once

typedef struct decimal64_t {
    uint64_t mantissa;
    int32_t exponent;
} decimal64_t;

decimal64_t dtofdec64(const uint64_t ieeeMant, const uint32_t ieeeExp);

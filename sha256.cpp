//
// Created by mukul on 20-05-2023.
//
#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <time.h>

#define ROTR(x, n) (((x) >> (n)) | ((x) << (32 - (n))))
#define SHR(x, n) ((x) >> (n))
#define CH(x, y, z) (((x) & (y)) ^ (~(x) & (z)))
#define MAJ(x, y, z) (((x) & (y)) ^ ((x) & (z)) ^ ((y) & (z)))
#define EP0(x) (ROTR(x, 2) ^ ROTR(x, 13) ^ ROTR(x, 22))
#define EP1(x) (ROTR(x, 6) ^ ROTR(x, 11) ^ ROTR(x, 25))
#define SIG0(x) (ROTR(x, 7) ^ ROTR(x, 18) ^ SHR(x, 3))
#define SIG1(x) (ROTR(x, 17) ^ ROTR(x, 19) ^ SHR(x, 10))

// Initial hash values
const uint32_t initial_hash_values[8] = {
0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
};

// Constants used in the SHA-256 algorithm
const uint32_t constants[64] = {
        0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
        0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
        0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
        0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
        0xe49b69c1, 0xefbe4786, 0xfc19dc6,  0x240ca1cc,
        0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
        0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
        0xc6e00bf3, 0xd5a79147, 0x6ca6351,  0x14292967,
        0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
        0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
        0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3,
        0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
        0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5,
        0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
        0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
        0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
};


// Performs the SHA-256 compression function on a 512-bit block
void sha256_compress(uint32_t *state, const uint8_t *block) {
uint32_t W[64];
uint32_t a, b, c, d, e, f, g, h, T1, T2;

// Prepare the message schedule
for (int t = 0; t < 16; ++t)
W[t] = (block[t * 4] << 24) | (block[t * 4 + 1] << 16) | (block[t * 4 + 2] << 8) | block[t * 4 + 3];
for (int t = 16; t < 64; ++t)
W[t] = SIG1(W[t - 2]) + W[t - 7] + SIG0(W[t - 15]) + W[t - 16];

// Initialize the working variables
a = state[0];
b = state[1];
c = state[2];
d = state[3];
e = state[4];
f = state[5];
g = state[6];
h = state[7];

// Perform the main hash computation
for (int t = 0; t < 64; ++t) {
T1 = h + EP1(e) + CH(e, f, g) + constants[t] + W[t];
T2 = EP0(a) + MAJ(a, b, c);
h = g;
g = f;
f = e;
e = d + T1;
d = c;
c = b;
b = a;
a = T1 + T2;
}

// Update the state with the final values
state[0] += a;
state[1] += b;
state[2] += c;
state[3] += d;
state[4] += e;
state[5] += f;
state[6] += g;
state[7] += h;
}

// Performs padding and divides the input into 512-bit blocks for processing
void sha256(const uint8_t *message, uint32_t *digest) {
    uint8_t padded_message[64];
    uint64_t message_length = strlen((const char *)message);
    uint64_t bit_length = message_length * 8;

    // Initialize the hash state
    uint32_t state[8];
    memcpy(state, initial_hash_values, sizeof(initial_hash_values));

    // Process each 512-bit block
    for (uint64_t i = 0; i < message_length / 64; ++i) {
        memcpy(padded_message, message + i * 64, 64);
        sha256_compress(state, padded_message);
    }

    // Pad the last block
    uint64_t last_block_length = message_length % 64;
    memcpy(padded_message, message + (message_length / 64) * 64, last_block_length);
    padded_message[last_block_length] = 0x80;
    if (last_block_length < 56) {
        memset(padded_message + last_block_length + 1, 0, 55 - last_block_length);
        padded_message[56] = (uint8_t)(bit_length >> 56);
        padded_message[57] = (uint8_t)(bit_length >> 48);
        padded_message[58] = (uint8_t)(bit_length >> 40);
        padded_message[59] = (uint8_t)(bit_length >> 32);
        padded_message[60] = (uint8_t)(bit_length >> 24);
        padded_message[61] = (uint8_t)(bit_length >> 16);
        padded_message[62] = (uint8_t)(bit_length >> 8);
        padded_message[63] = (uint8_t)bit_length;
        sha256_compress(state, padded_message);
    } else {
        memset(padded_message + last_block_length + 1, 0, 63 - last_block_length);
        sha256_compress(state, padded_message);
        memset(padded_message, 0, 56);
        padded_message[56] = (uint8_t)(bit_length >> 56);
        padded_message[57] = (uint8_t)(bit_length >> 48);
        padded_message[58] = (uint8_t)(bit_length >> 40);
        padded_message[59] = (uint8_t)(bit_length >> 32);
        padded_message[60] = (uint8_t)(bit_length >> 24);
        padded_message[61] = (uint8_t)(bit_length >> 16);
        padded_message[62] = (uint8_t)(bit_length >> 8);
        padded_message[63] = (uint8_t)bit_length;
        sha256_compress(state, padded_message);
    }

    // Store the final hash value
    for (int i = 0; i < 8; ++i)
        digest[i] = state[i];
}

void uint32_to_uint8(const uint32_t *src, uint8_t *dst, size_t num_elements) {
    for (size_t i = 0; i < num_elements; ++i) {
        dst[i * 4] = (uint8_t)(src[i] >> 24);
        dst[i * 4 + 1] = (uint8_t)(src[i] >> 16);
        dst[i * 4 + 2] = (uint8_t)(src[i] >> 8);
        dst[i * 4 + 3] = (uint8_t)src[i];
    }
}
int main() {
    uint8_t message[] = "12345678901234567890123456789012";
    uint32_t digest[8];
    clock_t start_time = clock();
    for(int i=0;i<2000000;i++) {
        sha256(message, digest);
        uint32_to_uint8(digest,message,8);
        sha256(message, digest);
    }
    clock_t end_time = clock();
    double elapsed_time = (double)(end_time - start_time) / CLOCKS_PER_SEC;
    printf("Elapsed time: %.4f seconds\n", elapsed_time);

    printf("SHA-256 output: %s",message);
    for (int i = 0; i < 8; ++i)
        printf("%08x ", digest[i]);
    printf("\n");

    return 0;
}


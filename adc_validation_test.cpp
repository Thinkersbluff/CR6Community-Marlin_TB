// Simple test to validate ADC resolution consistency
#include "Marlin/src/HAL/HAL.h"

int main() {
    // Check that HAL_ADC_RESOLUTION is set correctly
    #ifdef HAL_ADC_RESOLUTION
        // ADC resolution should be 12 bits for STM32F1 with our changes
        static_assert(HAL_ADC_RESOLUTION == 12, "Expected 12-bit ADC resolution");
        
        // Verify HAL_ADC_RANGE calculation
        #define EXPECTED_RANGE (1 << HAL_ADC_RESOLUTION)
        static_assert(HAL_ADC_RANGE == EXPECTED_RANGE, "HAL_ADC_RANGE calculation error");
        
        return 0; // All checks passed
    #else
        #error "HAL_ADC_RESOLUTION not defined"
        return 1;
    #endif
}

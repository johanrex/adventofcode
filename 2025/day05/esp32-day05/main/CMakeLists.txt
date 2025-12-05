idf_component_register(
    SRCS "day05.cpp"
    PRIV_REQUIRES spi_flash
    INCLUDE_DIRS "."
)

# Ensure the component is compiled as C++17
target_compile_features(${COMPONENT_LIB} PUBLIC cxx_std_17)

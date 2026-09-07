OUT="test_outputs/docs_co2_cyclic_injection"
. tests/scripts/initialize_output_folders.sh $OUT
. tests/scripts/get_plopm.sh
pyopmnearwell -i examples/co2.toml -o $OUT -m single
plopm -i $OUT/CO2 -v sgas -m gif -dpi 1000 -gi 50 -gl 1 -fs 10,5 -yf .0f -fz 20 -cbn 6 -t "Cyclic injection" -fn $OUT/co2_gas

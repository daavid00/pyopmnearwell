OUT="test_outputs/docs_co2_cyclic_injection"
. tests/scripts/initialize_output_folders.sh $OUT
. tests/scripts/get_plopm.sh
pyopmnearwell -i examples/co2.toml -o $OUT -m single
plopm -i $OUT/CO2 -v sgas -m gif -dpi 1000 -interval 50 -loop 1 -d 10,5 -yformat .0f -f 20 -cnum 6 -t "Cyclic injection" -save $OUT/co2_gas

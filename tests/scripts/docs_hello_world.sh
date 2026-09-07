OUT="test_outputs/docs_hello_world"
. tests/scripts/initialize_output_folders.sh $OUT
. tests/scripts/get_plopm.sh
pyopmnearwell -i examples/h2o.toml -o $OUT -m single
plopm -i $OUT/H2O -v pressure -s ,,1 -t 'Top view at the end of the simulation' -c bwr -xf .0f -cbf .0f -fn $OUT/hello_world

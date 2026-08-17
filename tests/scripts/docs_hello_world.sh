OUT="test_outputs/docs_hello_world"
. tests/scripts/initialize_output_folders.sh $OUT
. tests/scripts/get_plopm.sh
pyopmnearwell -i examples/h2o.toml -o $OUT -m single
plopm -i $OUT/H2O -v pressure -s ,,1 -t 'Top view at the end of the simulation' -c bwr -xformat .0f -cformat .0f -save $OUT/hello_world

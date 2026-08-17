NCPUS=${1:-16}
OUT="test_outputs/paper_salt_precipitation"
. tests/scripts/initialize_output_folders.sh $OUT
. tests/scripts/get_plopm.sh
mkdir "test_outputs/paper_salt_precipitation"
cp -r publications/Impact_of_Intermittency_on_Salt_Precipitation_During_CO2_Injection_2024_SPE/. $OUT
sed -i.bak "s/NPRUNS = 16/NPRUNS = $NCPUS/g" $OUT/case4/including_salt_precipitation/run_simulations.py && rm -f $OUT/case4/including_salt_precipitation/run_simulations.py.bak
sed -i.bak "s/NPRUNS = 16/NPRUNS = $NCPUS/g" $OUT/case4/neglecting_salt_precipitation/run_simulations.py && rm -f $OUT/case4/neglecting_salt_precipitation/run_simulations.py.bak
python3 $OUT/case1/run_simulations.py &
python3 $OUT/case2/run_simulations.py &
python3 $OUT/case3/run_simulations.py &
wait
python3 $OUT/case4/run_all.py &
wait

files="
$OUT/case1/nca.png
"

missing_file="test_outputs/missing_publication_files.txt"
missing=0

printf '%s\n' "$files" | while IFS= read -r f; do
    [ -z "$f" ] && continue
    if [ ! -f "$f" ]; then
        echo "$f" >> "$missing_file"
        missing=$((missing + 1))
    fi
done

if [ "$missing" -eq 0 ]; then
    echo "All figures and files exist."
    return 0
else
    echo "$missing figure(s) or file(s) missing."
    echo "See $missing_file"
    return 1
fi

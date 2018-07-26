for i in $(seq 0 20)
do
	python generate_and_upload.py $i &
done

#!/bin/bash
#SBATCH --partition nocona
#SBATCH --nodes=1
#SBATCH --ntasks=4
#SBATCH --time=48:00:00
#SBATCH --mem-per-cpu=3994MB
#SBATCH --output=%x.o%j
#SBATCH --error=%x.e%j

export PATH=/home/akitazum/miniconda3/bin:$PATH


# find ph_* -name *JPG|awk '{print $1}' > names.in
# cat names.in |sed -e "s|/|_|g"|sed -e "s/\^/p/g" > names.out
# paste names.in names.out|awk '{print "cp "$1" "$2}'|sh

 for s in $(ls *JPG);do cat v05.py |sed -e "s/image.jpg/${s}/g"|/lustre/work/akitazum/miniconda3/bin/python -;done

grep [A-Z] *tsv|sed -e "s/:/\t/g"|grep -v Point|cat header - |sed -e "s/_RGB.tsv//"|> v05_RGB.all.txt



# prepare index file from pep fasta
java -Xmx3500M -cp [path of MSGFPlus.jar] edu.ucsd.msjava.msdbsearch.BuildSA -d orf.fa
# mk mscan dir and move associated file into it
mkdir mscan_db
mv [seq_name].rev* [seq_name].c* ./mscan_db
# revise mscan setting in jobs.json and conf.server.json

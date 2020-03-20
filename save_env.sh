conda env export | grep -v "^prefix: " > environment.yml
echo "Exported environment to environment.yaml"

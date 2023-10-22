cd Slayer07 && npm i && npm run prepare
cd - > /dev/null

find . -type d -name "*Worker*" | while read -r directory; do
    # Entramos no diretório
    cd "$directory" || continue

    # Executamos o comando desejado (por exemplo, 'ls')
    npm i && npm run prepare

    # Saímos do diretório para retornar ao diretório principal
    cd - > /dev/null
done
import json
from pathlib import Path

file_path_entrada = Path("capitulos") / f"4-1-2.json";
file_path_saida =   Path("exemplo.md")

def quill_to_md(path_do_arquivo, path_arquivo_saida):
    string_final = "";
    with path_do_arquivo.open("r", encoding="utf-8") as file:
        rawChapterData = file.read()

    jsonData = json.loads(rawChapterData);
    lista = jsonData["ops"]
    tamanho_lista = len(lista);

    i = 0;
    while i < tamanho_lista:
        if (i + 1 >= tamanho_lista):
            string_final = string_final + lista[i]["insert"];
            break
        
        if 'header' in lista[i+1]['attributes']:
            if (lista[i+1]['attributes']['header'] == 1):
                hashes = "# ";
            
            if (lista[i+1]['attributes']['header'] == 2):
                hashes = "## ";
            
            if (lista[i+1]['attributes']['header'] == 3):
                hashes = "### ";

            string_final = string_final + hashes + lista[i]["insert"] + lista[i+1]["insert"];
        
        if 'list' in lista[i+1]['attributes']:
            # lista de elementos entre \n
            temp = lista[i]["insert"].split("\n");

            if (len(temp) > 1):
                item_da_lista = temp[len(temp) - 1];
                temp.pop();
                intermediario = "\n".join(temp);
                intermediario += "\n";
            else:
                intermediario = ""

            if (lista[i+1]['attributes']["list"] == "ordered"):
                marcador = "1. "
            
            if (lista[i+1]['attributes']["list"] == "bullet"):
                marcador = "- "
            
            string_final = string_final + intermediario + marcador + item_da_lista + lista[i+1]["insert"];

        if 'bold' in lista[i+1]['attributes']:
            string_final = string_final + lista[i]["insert"] + "**"  + lista[i+1]["insert"] + "**";
        
        if 'italic' in lista[i+1]['attributes']:
            string_final = string_final + lista[i]["insert"] + "*"  + lista[i+1]["insert"] + "*";
        
        if 'link' in lista[i+1]['attributes']:
            string_final = string_final + lista[i]["insert"] + f"<a href='${lista[i+1]['attributes']['link']}'>"  + lista[i+1]["insert"] + "</a>";
        
        #print(i, i+1);
        i += 2;

    with path_arquivo_saida.open("w", encoding="utf-8") as file:
        file.write(string_final)

    #print(jsonData);
    return string_final

string_final = quill_to_md(file_path_entrada, file_path_saida);
print(string_final)
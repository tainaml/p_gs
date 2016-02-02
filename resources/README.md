# README


## Problemas com gulp

Sempre que for fazer uma modificação rodar o comando `npm run build` para
gerar os assets e fazer o hash dos mesmos

### Problemas no carramentos de algum script após o passo acima

Geralmente esse problema é ocasionado pela alteração na referência do script,
adicionar o `/static/` antes do `javascripts/` dentro do "shared-[hash].js"
em static/javascripts.

# README


## Problemas com gulp

Sempre que for fazer uma modificação rodar o comando `npm run build` para
gerar os assets e fazer o hash dos mesmos

### Problemas no carramentos de algum script após o passo acima

Geralmente esse problema é ocasionado pela alteração na referência do script,
adicionar o `/static/` antes do `javascripts/` dentro do "shared-[hash].js"
em static/javascripts.


## instalando o npm para ao usuário

sudo chown -R $(whoami) ~/.npm
[more here](http://stackoverflow.com/questions/16151018/npm-throws-error-without-sudo)

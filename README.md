# Testes na plataforma Bluemix

Exemplo de utilização da Watson API e SQL Database Service. Este projeto utilizou o boilerplate [Personality Insights](https://github.com/watson-developer-cloud/personality-insights-python) como starter. 

Acesse a [aplicação exemplo](http://tcosta-pi.mybluemix.net/).

## Funcionamento
- Último insight salvo aparecerá na tela
- Cole o texto, **em inglês** na caixa de texto
- Veja os resultados da inferência nos gráficos
- Clique em **Salvar insights**, para armazenar o insight do texto atual no banco de dados

## Experiência no Bluemix
- Muito fácil configurar a aplicação Python para utilizar os serviços e testar localmente
- Ferramenta `cf` facilita muito o deploy
- De início, iria fazer a aplicação em Java, mas abortei por problemas para configurar o Liberty
- Boilerplates Java no catalogo Bluemix são construídos com ANT. Acho que deveria ser padronizado com Maven ou Gradle, com profiles configurados para rodar a aplicação local e no Bluemix, já que gerenciamento de dependências com application server é crítico, por causa de conflitos de bibliotecas e problemas de classloader, por exemplo. Certamente afeta a experiência de uso por programadores Java.
- Testei o serviço *retrieve and rank*, mas não cheguei a incluir nesse projeto.
  - Consulta no Solr com a [relevância padrão](https://gateway.watsonplatform.net/retrieve-and-rank/api/v1/solr_clusters/sc2c10509d_f73f_4378_b879_e5f8228cf7f5/solr/example-collection/select?q=what%20is%20the%20basic%20mechanism%20of%20the%20transonic%20aileron%20buzz&wt=json&fl=id,title)
  - Consulta com o [ranker treinado](https://gateway.watsonplatform.net/retrieve-and-rank/api/v1/solr_clusters/sc2c10509d_f73f_4378_b879_e5f8228cf7f5/solr/example-collection/fcselect?ranker_id=9849D6-rank-73&q=what%20is%20the%20basic%20mechanism%20of%20the%20transonic%20aileron%20buzz&wt=json&fl=id,title)

## Referências

- https://github.com/watson-developer-cloud/personality-insights-python

- http://www.ibm.com/smarterplanet/us/en/ibmwatson/developercloud/doc/retrieve-rank/get_start.shtml

- http://www.ibm.com/smarterplanet/us/en/ibmwatson/developercloud/retrieve-rank.html

- https://github.com/watson-developer-cloud/retrieve-and-rank-java
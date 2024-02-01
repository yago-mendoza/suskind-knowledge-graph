# Suskind Knowledge Graph

This project introduces a graph-based framework designed to complement traditional Natural Language Processing (NLP) models. Central to this approach is a dynamic graph where nodes are featured entities, interconnected with contextual relevance. This structure allows for a nuanced understanding of relationships and context, offering precision beyond linear text analysis. The database is the culmination of three years of  data collection, manually undertaken to ensure quality. To facilitate user interaction, multiple Command Line Interfaces (CLI) makes database management intuitive. It also incorporates algorithms of graph search that can be configured on the fly, further enhancing its adaptability and utility for diverse data interaction needs.

## Documentation
The following [documentation](https://yago-mendoza.gitbook.io/suskind_knowledge_graph/) provides an exhaustive study of all components of the system, especially those related with the CLIs interaction.


## Roadmap

- **Database Preparation**
  - ~~Cleaning Initial Node Database~~

- **SK Components Dessign**
  - ~~Design of Node Class~~
  - ~~Design of NodeSet~~
  - ~~Design of Graph~~

- **Implementation of Search Algorithms**
  - ~~Design of Centrality Algorithm~~
  - ~~Development of Density Search Algorithm~~
  - ~~Optional Design of Shortest Path Algorithm~~

- ~~Organizing All Files into a Single Directory~~

- **Development of Main Command Line Interface (CLI)**
  - ~~Implementation of Basic Commands (cd, ls, etc.)~~
  - ~~Development of Helper Functions~~
  - ~~Creation of User Interfaces for Specific Functions~~
  - ~~**Design of Auxiliary CLIs**~~
    - ~~LS_Interface~~
    - ~~VG_Interface~~
    - ~~NW_Interface~~
    - ~~GB_Interface~~
  - ~~Integration of Centrality, Density Search, and Shortest Path Algorithms~~
  - ~~Edge cases testing.~~

- **AI for data processing**
  - Study existing heuristic methods applicable to network analysis.
  - Create a test corpus aligned with the principles of "atomicity" and "proximity".
    
  - **Large Language Model (LLM) Integration**
    - Research and select an appropriate LLM for the task.
    - Dessign the display to rate the success (granularity + contextual placement).
    - **Testing and Validation**
      - Implement the heuristic model on a subset of data.
      - Monitor performance and adjust prompting to maximize success rate.
        
- **CLI Integration**
  - Dessign a pipeline that connects AI generative capabilities with a gateway on CLI.
  - Test success rate with updated tooling.

## Execution

```bash
  py -i main.py
```
    
## License

[MIT](https://choosealicense.com/licenses/mit/)


## 🔗 Links

[![portfolio](https://img.shields.io/badge/my_portfolio-000?style=for-the-badge&logo=ko-fi&logoColor=white)](https://github.com/yago-mendoza)
[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/yago-mendoza)
[![twitter](https://img.shields.io/badge/twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white)](https://twitter.com/ymdatweets)

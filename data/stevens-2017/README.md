# Structures from Stevens et al. 2017

- Title: *3D structures of individual mammalian genomes studied by single-cell Hi-C*
- DOI: [https://doi.org/10.1038/nature21429](https://doi.org/10.1038/nature21429)
- GEO: [GSE80280](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE80280)
- Organism: Mus musculus

<div align="center">
  
|List of structures (with links)|
| :---: |
| [structures.md](./structures.md) |

</div>

---

Process:
- Downloaded `GSE80280_RAW.tar` (19.7 Gb) from the GEO repository.
- Copied only the cell structures (identified by the `.pdb` file).

Run the notebook for data processing using [juv](https://github.com/manzt/juv). 
```sh
cd stevens-2017
juv run notebook.ipynb
```

---

TODO:
- [x] make it a model:
    - [x] store bin chromosomes
    - [x] store bin coordinates
        - [ ] make sure coordinates are correct
- [ ] figure out what the multiple structures in single PDB mean

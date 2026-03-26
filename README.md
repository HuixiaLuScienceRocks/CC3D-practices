# Installing CC3D in UBUNTU24.04.3
```
conda create -n cc3d_460 python=3.10
```
```
conda activate cc3d_460
```
```
conda install -c conda-forge mamba=2.1.1
```

```
mamba install -c main -c conda-forge -c compucell3d compucell3d=4.6.0
```

```
python -m cc3d.player5
```

```
conda deactivate
```


I) In the folder of "new_simulation_cc3d_01_31_2025_16_52_4.."
1. Folder new_simulation_cc3d_01_31_2025_16_52_40_c61075 is about CellSort
2. In this practice I am trying to generate restart files so I can continue running the CC3D simulation from a checkpoint
3. Ticking "Allow multiple restart snapshots" will allow generating multiple checkpoint files
4. in setup.png you can see by setting the correct path, we can generate the restart files and energy.log files correctly which gave me problems at the beginning. Please make sure they are inconsistent

II) In the folder of "Exercise 2 Cell Growth", it simulates cell growth, in this simulation one cell can keep growing until double of its target volume (25) and then it will divide into two cells, indicated by these fourlines of code: 
        cells_to_divide=[]
        for cell in self.cell_list:
            if cell.volume>50:
                cells_to_divide.append(cell)
                
   

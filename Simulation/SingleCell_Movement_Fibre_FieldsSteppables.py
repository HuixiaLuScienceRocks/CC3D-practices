from cc3d.core.PySteppables import *
import numpy as np
import random
from random import uniform

class SingleCell_Movement_Fibre_FieldsSteppable(SteppableBasePy):
    
    def __init__(self, frequency=1):

        SteppableBasePy.__init__(self,frequency)

    def start(self):
        """
        Called before MCS=0 while building the initial simulation
        """
        
        field = self.field.ECM_Field
        field_angle = self.field.ECM_Field_Angle
        field_fibrenumber = self.field.ECM_Field_FibreNumber
               
        # Random lines (can overlap)
        
        # n_line = 10000
        # n_line = 1
        n_line = 100
        length = 80
             
        global fibre_to_angle
        fibre_to_angle = list([])
      
        for v in range(0, n_line):
            x_start = uniform(0, self.dim.x)
            y_start = uniform(0, self.dim.y)
            # angle = 0.0
            # angle = np.pi/2
            angle = uniform(0, 2*np.pi)
            fibre_to_angle.append(angle)
            x_end = x_start + length*np.cos(angle)
            y_end = y_start + length*np.sin(angle)
            for r in np.linspace(0, length):
                x = x_start + r*np.cos(angle)
                y = y_start + r*np.sin(angle)
                if (x >= self.dim.x):
                    x = x - self.dim.x
                if (x <= self.dim.x):
                    x = x + self.dim.x   
                if (y >= self.dim.y):
                    y = y - self.dim.y
                if (y <= self.dim.y):
                    y = y + self.dim.y
                field[x,y,0] = 5.0
                field_angle[x,y,0] = angle
                field_fibrenumber[x,y,0] = v
        
        self.cell_field[10:20, (self.dim.y/2)-2:(self.dim.y/2)+2, 0] = self.new_cell(self.CELL)
       
        for cell in self.cellList:
            cd = self.chemotaxisPlugin.addChemotaxisData(cell, "ECM_Field")
            # cd.setLambda(0.0)
            cd.setLambda(1E10)
            # cd.setLambda(-1E10)
            cd.assignChemotactTowardsVectorTypes([self.MEDIUM]) 
            cell_angle = 0.0
            # cell_angle = uniform(0, 2*np.pi)
            cell.dict['theta'] = cell_angle
            cell.lambdaVecX = -10.0*np.cos(cell.dict['theta'])
            cell.lambdaVecY = -10.0*np.sin(cell.dict['theta'])
                
        for cell in self.cell_list:
            cell.dict["Old_pos"] = [cell.xCOM,cell.yCOM,cell.zCOM]
            
        self.plot_win = self.add_new_plot_window(title='Ave-Velocity-x vs. mcs',
                                                 x_axis_title='MonteCarlo Step (MCS)',
                                                 y_axis_title='Ave-Velocity-x', x_scale_type='linear', y_scale_type='linear',
                                                 grid=False)
        self.plot_win.add_plot("Ave_Velocity_x", style='Lines', color='red', size=5)
        
        self.plot_win2 = self.add_new_plot_window(title='Ave-Velocity-y vs. mcs',
                                                 x_axis_title='MonteCarlo Step (MCS)',
                                                 y_axis_title='Ave-Velocity-y', x_scale_type='linear', y_scale_type='linear',
                                                 grid=False)
        self.plot_win2.add_plot("Ave_Velocity_y", style='Lines', color='red', size=5)
        
        # self.plot_win3 = self.add_new_plot_window(title='Ave-Velocity-z vs. mcs',
                                                 # x_axis_title='MonteCarlo Step (MCS)',
                                                 # y_axis_title='Ave-Velocity-z', x_scale_type='linear', y_scale_type='linear',
                                                 # grid=False)
        # self.plot_win.add_plot("Ave_Velocity_z", style='Lines', color='yellow', size=5)

    def step(self, mcs):
        """
        Called every frequency MCS while executing the simulation
        
        :param mcs: current Monte Carlo step
        """
        
        # n_line = 10000
        # n_line = 1
        n_line = 200
        length = 10
        
        thres = 0.5
        
        field = self.field.ECM_Field
        field_angle = self.field.ECM_Field_Angle
        field_fibrenumber = self.field.ECM_Field_FibreNumber
        
        if mcs%1 == 0:
        # if mcs%50 == 0:
            
            for cell in self.cell_list:
                secretor = self.get_field_secretor("ECM_Field")
                amount_seen = secretor.amountSeenByCell(cell)
                if amount_seen > thres:
                    
                    cell.lambdaVecX = -10.0
                    cell.lambdaVecY = 0.0
                    
                    # fibre_angle = 0
                    # fibre_angle = np.pi / 2
                    # fibre_angle = np.random.uniform(0,2*np.pi)
                    
                    '''
                    pixelList = CellPixelList(self.pixelTrackerPlugin,cell)
                    list_fibres = []
                    amount_pixels_fibres = [0] * n_line
                    for pixelData in pixelList:
                        pt=pixelData.pixel
                        x = pt.x
                        y = pt.y
                        z = pt.z
                        if (field[x,y,0] == 5.0):
                            list_fibres.append(int(field_fibrenumber[x,y,0]))
                            amount_pixels_fibres[int(field_fibrenumber[x,y,0])] =+ 1    
                            
                    list_fibres2 = sorted(set(list_fibres))   
                    
                    angle = 0.0
                    if len(list_fibres2) != 0:
                        v = amount_pixels_fibres.index(max(amount_pixels_fibres))
                        angle = fibre_to_angle[v]
                    
                    fibre_angle = angle   
                                        
                    cell_angle = cell.dict['theta']
                    
                    if ( np.abs( (cell_angle - fibre_angle) % np.pi ) < (np.pi / 2) ):
                        cell_angle = fibre_angle
                    else:
                        cell_angle = -fibre_angle
                                    
                                    
                    cell.dict['theta'] = cell_angle
                    cell.lambdaVecX = -5.0*np.cos(cell.dict['theta'])
                    cell.lambdaVecY = -5.0*np.sin(cell.dict['theta'])    
                    
                    '''
                    
                else:
                    cell.lambdaVecX = 0.0
                    cell.lambdaVecY = -10.0
                
        if mcs%500 == 0:
            
            for cell in self.cell_list:
                
                Current_pos = [cell.xCOM,cell.yCOM,cell.zCOM]
                
                Vx = Current_pos[0] - cell.dict["Old_pos"][0]
                Vy = Current_pos[1] - cell.dict["Old_pos"][1]
                Vz = Current_pos[2] - cell.dict["Old_pos"][2]
            
                cell.dict["Old_pos"][0] = Current_pos[0] #COMPUCELL
                cell.dict["Old_pos"][1] = Current_pos[1]
                cell.dict["Old_pos"][2] = Current_pos[2]
                
                self.plot_win.add_data_point("Ave_Velocity_x", mcs, Vx)
                self.plot_win2.add_data_point("Ave_Velocity_y", mcs, Vy)
                # self.plot_win3.add_data_point("Ave_Velocity_z", mcs, Vz)
                      
    def finish(self):
        """
        Called after the last MCS to wrap up the simulation
        """

    def on_stop(self):
        """
        Called if the simulation is stopped before the last MCS
        """

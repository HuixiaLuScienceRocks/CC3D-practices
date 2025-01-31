from cc3d.core.PySteppables import *
import os
class CellSortDemoLecture3Steppable(SteppableBasePy):

    def __init__(self, frequency=1):
        SteppableBasePy.__init__(self, frequency)
        
        #Set paths for loading & saving simulation states
        self.previous_simulation_path = "/home/huixia/Desktop/computecell3d-workshop/NORA_PROJECT/previous_simulation/previous_simulation.cc3d"
        self.new_save_path = "/home/huixia/Desktop/computecell3d-workshop/NORA_PROJECT/new_simulation/simulation_state.cc3d"

    def start(self):
        """
        Loads a previous simulation if it exists; otherwise, starts a fresh simulation.
        """

        #Create first plot window (Contact between cell types) WITH LEGEND
        self.plot_win = self.add_new_plot_window(title='Contact Area by Type',
                                                 x_axis_title='MonteCarlo Step (MCS)',
                                                 y_axis_title='Contact Area',
                                                 x_scale_type='linear', y_scale_type='linear',
                                                 grid=False, 
                                                 config_options={'legend': True})  #Legend added

        self.plot_win.add_plot("Dark-Dark", style='Lines', color='blue', size=5)
        self.plot_win.add_plot("Dark-Light", style='Lines', color='red', size=5)
        self.plot_win.add_plot("Light-Light", style='Lines', color='green', size=5)

        #Create second plot window (Contact with medium) WITH LEGEND
        self.plot_win2 = self.add_new_plot_window(title='Contact Area with Medium',
                                                  x_axis_title='MonteCarlo Step (MCS)',
                                                  y_axis_title='Contact Area',
                                                  x_scale_type='linear', y_scale_type='linear',
                                                  grid=False, 
                                                  config_options={'legend': True})  # Legend added

        self.plot_win2.add_plot("Dark-Medium", style='Lines', color='purple', size=5)
        self.plot_win2.add_plot("Light-Medium", style='Lines', color='orange', size=5)

    def step(self, mcs):
        if mcs % 10 == 0:  # Only plot every ten time steps
            """
            Calculate contact areas for each type pair
            """
            # Create placeholders to accumulate areas
            ADD = 0.0  # Dark-Dark
            ADL = 0.0  # Dark-Light
            ALL = 0.0  # Light-Light
            ADM = 0.0  # Dark-Medium
            ALM = 0.0  # Light-Medium

            for cell in self.cell_list:  # Loop over all cells
                if cell:  # Skip if the cell is medium
                    for neighbor, common_surface_area in self.get_cell_neighbor_data_list(cell):
                        if neighbor:  # Neighbor is a cell, not medium
                            if cell.type == self.DARK:
                                if neighbor.type == self.DARK:
                                    ADD += common_surface_area
                                else:
                                    ADL += common_surface_area
                            else:
                                if neighbor.type == self.LIGHT:
                                    ALL += common_surface_area
                                else:
                                    ADL += common_surface_area
                        else:  # Neighbor is medium
                            if cell.type == self.DARK:
                                ADM += common_surface_area
                            else:
                                ALM += common_surface_area

            # Correct for Double Counting of cell-cell contact
            ADD /= 2.0
            ADL /= 2.0
            ALL /= 2.0

            # Plot the values of the five contacts
            self.plot_win.add_data_point("Dark-Dark", mcs, ADD)
            self.plot_win.add_data_point("Dark-Light", mcs, ADL)
            self.plot_win.add_data_point("Light-Light", mcs, ALL)

            self.plot_win2.add_data_point("Dark-Medium", mcs, ADM)
            self.plot_win2.add_data_point("Light-Medium", mcs, ALM)

    def finish(self):
        """
        Saves the final state of the simulation.
        """
        

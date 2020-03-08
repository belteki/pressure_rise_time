# Effect of Pressure Rise Time on Ventilator Parameters and Gas Exchange During Neonatal Ventilation
This is the github repository for the code that accompanies the paper 
"Effect of Pressure Rise Time on Ventilator Parameters and Gas Exchange During Neonatal Ventilation" 
Authors: David Chong, Sabrina Kayser, Eniko Szakmar, Colin J Morley, & Gusztav Belteki, Pediatric Pulmonology, in press. 
A description of the scripts can be found below.
### Pre-processing
- combineTCMdata.py was used to combine multiple transcutaneous monitoring data files into 1 and to parse the time stamps into milliseconds
- EF_combine_FCTR.py was used to combine the capnography data files into 1 and to parse the time stamps into milliseconds
- generateSettingsGroupIndex.py was used to parse the ventilator settings (slow_Setting_) files for each patient and determine the time in milliseconds whenever the slope and ventilation mode was changed to allow extraction of relevant information into these groups for comparison
- groupdata.py was used to extract the various physiological parameters that were monitored based on the time periods identified with generateSettingsGroupIndex.py and to calculate the mean and standard deviation of those parameters over those periods
### Data Analysis
- table2.py was used to calculate the repeated measures ANOVA on each physiological parameter and identify the ones with a significant change across different slope times.
- table3.py was used to calculate the linear regression values for the physiological parameters that changed significantly across different slope times.
### Figure Generation
- Figure1.py was used to generate example breaths with annotated inspiratory and expiratory periods as well as inspiratory hold if present for each extreme in slope time for each ventilation mode
- Figure2.py was used to plot the regression lines for physiological parameters that were identified to be significantly changing over the range of slope times.
- Figure3.py was used to plot the change in oxygen saturations and end tidal CO2 levels across the different slope times and ventilation modes
- supplementaryplots.py was used to plot the end tidal CO2 trends for each individual patient across the different slope times and ventilation modes
- bloodgas_etco2.py was used to plot the correlation between the measured end tidal CO2 and the pCO2 levels as measured using blood gas.

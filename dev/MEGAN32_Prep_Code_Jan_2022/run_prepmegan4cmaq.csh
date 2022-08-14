#!/bin/csh
foreach dom ( SE_US )

./prepmegan4cmaq_grwform.x < prepmegan4cmaq.growthform.inp | tee -a grwform.$dom.log
mv ./output/grid_growth_form.csv ./output/grid_growth_form.$dom.csv

./prepmegan4cmaq_ecotype.x < prepmegan4cmaq.ecotype.inp | tee -a ecotype.$dom.log
mv ./output/grid_ecotype.csv ./output/grid_ecotype.$dom.csv

./prepmegan4cmaq_cantype.x < prepmegan4cmaq.cantype.inp | tee -a cantype.$dom.log
mv ./output/CT3.csv ./output/CT3.$dom.csv

./prepmegan4cmaq_lai.x < prepmegan4cmaq.lai.$dom.inp | tee -a lai.$dom.log
mv ./output/LAI3.csv ./output/LAI3.$dom.csv

./prepmegan4cmaq_w126.x < prepmegan4cmaq.soil.$dom.inp | tee -a w126.$dom.log
mv ./output/grid_W126.csv ./output/grid_W126.$dom.csv

./prepmegan4cmaq_arid.x < prepmegan4cmaq.soil.$dom.inp | tee -a arid.$dom.log
mv ./output/grid_arid.csv ./output/grid_arid.$dom.csv

./prepmegan4cmaq_non_arid.x < prepmegan4cmaq.soil.$dom.inp | tee -a non_arid.$dom.log
mv ./output/grid_non_arid.csv ./output/grid_non_arid.$dom.csv

./prepmegan4cmaq_landtype.x < prepmegan4cmaq.soil.$dom.inp | tee -a landtype.$dom.log
mv ./output/grid_LANDTYPE.csv ./output/grid_LANDTYPE.$dom.csv

./prepmegan4cmaq_fert.x < prepmegan4cmaq.soil.$dom.inp | tee -a fert.$dom.log
mv ./output/grid_FERT.csv ./output/grid_FERT.$dom.csv

./prepmegan4cmaq_nitrogen.x < prepmegan4cmaq.soil.$dom.inp | tee -a nitrogen.$dom.log
mv ./output/grid_NITROGEN.csv ./output/grid_NITROGEN.$dom.csv

end

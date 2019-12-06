<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE eagle SYSTEM "eagle.dtd">
<eagle version="9.5.2">
<drawing>
<settings>
<setting alwaysvectorfont="no"/>
<setting verticaltext="up"/>
</settings>
<grid distance="0.1" unitdist="inch" unit="inch" style="lines" multiple="1" display="no" altdistance="0.01" altunitdist="inch" altunit="inch"/>
<layers>
<layer number="1" name="Top" color="4" fill="1" visible="no" active="no"/>
<layer number="16" name="Bottom" color="1" fill="1" visible="no" active="no"/>
<layer number="17" name="Pads" color="2" fill="1" visible="no" active="no"/>
<layer number="18" name="Vias" color="2" fill="1" visible="no" active="no"/>
<layer number="19" name="Unrouted" color="6" fill="1" visible="no" active="no"/>
<layer number="20" name="Dimension" color="24" fill="1" visible="no" active="no"/>
<layer number="21" name="tPlace" color="7" fill="1" visible="no" active="no"/>
<layer number="22" name="bPlace" color="7" fill="1" visible="no" active="no"/>
<layer number="23" name="tOrigins" color="15" fill="1" visible="no" active="no"/>
<layer number="24" name="bOrigins" color="15" fill="1" visible="no" active="no"/>
<layer number="25" name="tNames" color="7" fill="1" visible="no" active="no"/>
<layer number="26" name="bNames" color="7" fill="1" visible="no" active="no"/>
<layer number="27" name="tValues" color="7" fill="1" visible="no" active="no"/>
<layer number="28" name="bValues" color="7" fill="1" visible="no" active="no"/>
<layer number="29" name="tStop" color="7" fill="3" visible="no" active="no"/>
<layer number="30" name="bStop" color="7" fill="6" visible="no" active="no"/>
<layer number="31" name="tCream" color="7" fill="4" visible="no" active="no"/>
<layer number="32" name="bCream" color="7" fill="5" visible="no" active="no"/>
<layer number="33" name="tFinish" color="6" fill="3" visible="no" active="no"/>
<layer number="34" name="bFinish" color="6" fill="6" visible="no" active="no"/>
<layer number="35" name="tGlue" color="7" fill="4" visible="no" active="no"/>
<layer number="36" name="bGlue" color="7" fill="5" visible="no" active="no"/>
<layer number="37" name="tTest" color="7" fill="1" visible="no" active="no"/>
<layer number="38" name="bTest" color="7" fill="1" visible="no" active="no"/>
<layer number="39" name="tKeepout" color="4" fill="11" visible="no" active="no"/>
<layer number="40" name="bKeepout" color="1" fill="11" visible="no" active="no"/>
<layer number="41" name="tRestrict" color="4" fill="10" visible="no" active="no"/>
<layer number="42" name="bRestrict" color="1" fill="10" visible="no" active="no"/>
<layer number="43" name="vRestrict" color="2" fill="10" visible="no" active="no"/>
<layer number="44" name="Drills" color="7" fill="1" visible="no" active="no"/>
<layer number="45" name="Holes" color="7" fill="1" visible="no" active="no"/>
<layer number="46" name="Milling" color="3" fill="1" visible="no" active="no"/>
<layer number="47" name="Measures" color="7" fill="1" visible="no" active="no"/>
<layer number="48" name="Document" color="7" fill="1" visible="no" active="no"/>
<layer number="49" name="Reference" color="7" fill="1" visible="no" active="no"/>
<layer number="51" name="tDocu" color="7" fill="1" visible="no" active="no"/>
<layer number="52" name="bDocu" color="7" fill="1" visible="no" active="no"/>
<layer number="88" name="SimResults" color="9" fill="1" visible="yes" active="yes"/>
<layer number="89" name="SimProbes" color="9" fill="1" visible="yes" active="yes"/>
<layer number="90" name="Modules" color="5" fill="1" visible="yes" active="yes"/>
<layer number="91" name="Nets" color="2" fill="1" visible="yes" active="yes"/>
<layer number="92" name="Busses" color="1" fill="1" visible="yes" active="yes"/>
<layer number="93" name="Pins" color="2" fill="1" visible="no" active="yes"/>
<layer number="94" name="Symbols" color="4" fill="1" visible="yes" active="yes"/>
<layer number="95" name="Names" color="7" fill="1" visible="yes" active="yes"/>
<layer number="96" name="Values" color="7" fill="1" visible="yes" active="yes"/>
<layer number="97" name="Info" color="7" fill="1" visible="yes" active="yes"/>
<layer number="98" name="Guide" color="6" fill="1" visible="yes" active="yes"/>
</layers>
<schematic xreflabel="%F%N/%S.%C%R" xrefpart="/%S.%C%R">
<libraries>
<library name="Bikota">
<packages>
<package name="LIS3DH">
<pad name="P$1" x="-8.89" y="-8.89" drill="1" shape="square"/>
<pad name="P$2" x="-6.35" y="-8.89" drill="1" shape="square"/>
<pad name="P$3" x="-3.81" y="-8.89" drill="1" shape="square"/>
<pad name="P$4" x="-1.27" y="-8.89" drill="1" shape="square"/>
<pad name="P$5" x="1.27" y="-8.89" drill="1" shape="square"/>
<pad name="P$6" x="3.81" y="-8.89" drill="1" shape="square"/>
<pad name="P$7" x="6.35" y="-8.89" drill="1" shape="square"/>
<pad name="P$8" x="8.89" y="-8.89" drill="1" shape="square"/>
<wire x1="-10.16" y1="-10.16" x2="10.16" y2="-10.16" width="0.3048" layer="21"/>
<wire x1="10.16" y1="-10.16" x2="10.16" y2="10.16" width="0.3048" layer="21"/>
<wire x1="-10.16" y1="10.16" x2="10.16" y2="10.16" width="0.3048" layer="21"/>
<wire x1="-10.16" y1="-10.16" x2="-10.16" y2="10.16" width="0.3048" layer="21"/>
<text x="-3.048" y="-0.635" size="1.27" layer="21">LIS3DH</text>
</package>
<package name="BN220">
<pad name="P$1" x="0" y="3.81" drill="1" shape="square"/>
<pad name="P$2" x="0" y="1.27" drill="1" shape="square"/>
<pad name="P$3" x="0" y="-1.27" drill="1" shape="square"/>
<pad name="P$4" x="0" y="-3.81" drill="1" shape="square"/>
<wire x1="-1.27" y1="5.08" x2="1.27" y2="5.08" width="0.127" layer="21"/>
<wire x1="1.27" y1="5.08" x2="1.27" y2="-5.08" width="0.127" layer="21"/>
<wire x1="1.27" y1="-5.08" x2="-1.27" y2="-5.08" width="0.127" layer="21"/>
<wire x1="-1.27" y1="-5.08" x2="-1.27" y2="5.08" width="0.127" layer="21"/>
</package>
<package name="BME280">
<pad name="P$1" x="0" y="6.35" drill="1" shape="square"/>
<pad name="P$2" x="0" y="3.81" drill="1" shape="square"/>
<pad name="P$3" x="0" y="1.27" drill="1" shape="square"/>
<pad name="P$4" x="0" y="-1.27" drill="1" shape="square"/>
<pad name="P$5" x="0" y="-3.81" drill="1" shape="square"/>
<pad name="P$6" x="0" y="-6.35" drill="1" shape="square"/>
<wire x1="-1.27" y1="7.62" x2="1.27" y2="7.62" width="0.127" layer="21"/>
<wire x1="1.27" y1="7.62" x2="1.27" y2="-7.62" width="0.127" layer="21"/>
<wire x1="1.27" y1="-7.62" x2="-1.27" y2="-7.62" width="0.127" layer="21"/>
<wire x1="-1.27" y1="-7.62" x2="-1.27" y2="7.62" width="0.127" layer="21"/>
</package>
<package name="ESP32T-CALL">
<pad name="ESP32_3V3" x="29.21" y="13.22501875" drill="1.100075" diameter="1.6764" shape="square" rot="R180"/>
<pad name="P$2" x="26.67" y="13.22501875" drill="1.100075" diameter="1.6764" shape="square" rot="R180"/>
<pad name="SVP" x="24.13" y="13.22501875" drill="1.100075" diameter="1.6764" shape="square" rot="R180"/>
<pad name="GPIO34" x="19.05" y="13.22501875" drill="1.100075" diameter="1.6764" shape="square" rot="R180"/>
<pad name="GPIO35" x="16.51" y="13.22501875" drill="1.100075" diameter="1.6764" shape="square" rot="R180"/>
<pad name="GPIO32" x="13.97" y="13.22501875" drill="1.100075" diameter="1.6764" shape="square" rot="R180"/>
<pad name="GPIO33" x="11.43" y="13.22501875" drill="1.100075" diameter="1.6764" shape="square" rot="R180"/>
<pad name="GPIO25" x="8.89" y="13.22501875" drill="1.100075" diameter="1.6764" shape="square" rot="R180"/>
<pad name="GPIO26" x="6.35" y="13.22501875" drill="1.100075" diameter="1.6764" shape="square" rot="R180"/>
<pad name="GPIO27" x="3.81" y="13.22501875" drill="1.100075" diameter="1.6764" shape="square" rot="R180"/>
<pad name="GPIO14" x="1.27" y="13.22501875" drill="1.100075" diameter="1.6764" shape="square" rot="R180"/>
<pad name="GPIO12" x="-1.27" y="13.22501875" drill="1.100075" diameter="1.6764" shape="square" rot="R180"/>
<pad name="GND" x="-3.81" y="13.22501875" drill="1.100075" diameter="1.6764" shape="square" rot="R180"/>
<pad name="GPIO13" x="-6.35" y="13.22501875" drill="1.100075" diameter="1.6764" shape="square" rot="R180"/>
<pad name="SD2" x="-8.89" y="13.22501875" drill="1.100075" diameter="1.6764" shape="square" rot="R180"/>
<pad name="SD3" x="-11.43" y="13.22501875" drill="1.100075" diameter="1.6764" shape="square" rot="R180"/>
<pad name="CMD" x="-13.97" y="13.22501875" drill="1.100075" diameter="1.6764" shape="square" rot="R180"/>
<pad name="ESP32_5V" x="-16.51" y="13.22501875" drill="1.100075" diameter="1.6764" shape="square" rot="R180"/>
<pad name="SPK+" x="-19.05" y="13.22501875" drill="1.100075" diameter="1.6764" shape="square" rot="R180"/>
<pad name="SPK-" x="-21.59" y="13.22501875" drill="1.100075" diameter="1.6764" shape="square" rot="R180"/>
<hole x="34.27" y="12.445" drill="2.99999375"/>
<pad name="GND3" x="29.21" y="-13.22501875" drill="1.100075" diameter="1.6764" shape="square" rot="R180"/>
<pad name="GPIO23" x="26.67" y="-13.22501875" drill="1.100075" diameter="1.6764" shape="square" rot="R180"/>
<pad name="GPIO22" x="24.13" y="-13.22501875" drill="1.100075" diameter="1.6764" shape="square" rot="R180"/>
<pad name="TXD" x="21.59" y="-13.22501875" drill="1.100075" diameter="1.6764" shape="square" rot="R180"/>
<pad name="RXD" x="19.05" y="-13.22501875" drill="1.100075" diameter="1.6764" shape="square" rot="R180"/>
<pad name="GPIO21" x="16.51" y="-13.22501875" drill="1.100075" diameter="1.6764" shape="square" rot="R180"/>
<pad name="GND2" x="13.97" y="-13.22501875" drill="1.100075" diameter="1.6764" shape="square" rot="R180"/>
<pad name="GPIO19" x="11.43" y="-13.22501875" drill="1.100075" diameter="1.6764" shape="square" rot="R180"/>
<pad name="GPIO18" x="8.89" y="-13.22501875" drill="1.100075" diameter="1.6764" shape="square" rot="R180"/>
<pad name="GPIO5" x="6.35" y="-13.22501875" drill="1.100075" diameter="1.6764" shape="square" rot="R180"/>
<pad name="NC3" x="3.81" y="-13.22501875" drill="1.100075" diameter="1.6764" shape="square" rot="R180"/>
<pad name="NC2" x="1.27" y="-13.22501875" drill="1.100075" diameter="1.6764" shape="square" rot="R180"/>
<pad name="GPIO4" x="-1.27" y="-13.22501875" drill="1.100075" diameter="1.6764" shape="square" rot="R180"/>
<pad name="GPIO0" x="-3.81" y="-13.22501875" drill="1.100075" diameter="1.6764" shape="square" rot="R180"/>
<pad name="GPIO2" x="-6.35" y="-13.22501875" drill="1.100075" diameter="1.6764" shape="square" rot="R180"/>
<pad name="GPIO15" x="-8.89" y="-13.22501875" drill="1.100075" diameter="1.6764" shape="square" rot="R180"/>
<pad name="SD1" x="-11.43" y="-13.22501875" drill="1.100075" diameter="1.6764" shape="square" rot="R180"/>
<pad name="SD0" x="-13.97" y="-13.22501875" drill="1.100075" diameter="1.6764" shape="square" rot="R180"/>
<pad name="CLK" x="-16.51" y="-13.22501875" drill="1.100075" diameter="1.6764" shape="square" rot="R180"/>
<pad name="MIC-" x="-19.05" y="-13.22501875" drill="1.100075" diameter="1.6764" shape="square" rot="R180"/>
<pad name="MIC+" x="-21.59" y="-13.22501875" drill="1.100075" diameter="1.6764" shape="square" rot="R180"/>
<hole x="34.27" y="-12.445" drill="2.99999375"/>
<wire x1="-37.39" y1="-14.505" x2="37.39" y2="-14.505" width="0.127" layer="21"/>
<wire x1="37.39" y1="-14.505" x2="37.39" y2="14.505" width="0.127" layer="21"/>
<wire x1="-37.39" y1="14.505" x2="37.39" y2="14.505" width="0.127" layer="21"/>
<wire x1="-37.39" y1="-14.505" x2="-37.39" y2="14.505" width="0.127" layer="21"/>
<hole x="-35.09" y="12.395" drill="2.99999375"/>
<hole x="-35.09" y="-12.395" drill="2.99999375"/>
<wire x1="-32.385" y1="-9.525" x2="-24.13" y2="-9.525" width="0.127" layer="21"/>
<wire x1="-32.385" y1="-9.525" x2="-32.385" y2="-14.605" width="0.127" layer="21"/>
<wire x1="-24.13" y1="-9.525" x2="-24.13" y2="-14.605" width="0.127" layer="21"/>
<pad name="SVN" x="21.59" y="13.22501875" drill="1.100075" diameter="1.6764" shape="square"/>
</package>
<package name="MH-Z14A">
<pad name="P$1" x="0" y="2.54" drill="1" shape="square"/>
<pad name="P$2" x="0" y="0" drill="1" shape="square"/>
<pad name="P$3" x="0" y="-2.54" drill="1" shape="square"/>
<wire x1="-1.27" y1="3.81" x2="1.27" y2="3.81" width="0.127" layer="21"/>
<wire x1="1.27" y1="3.81" x2="1.27" y2="-3.81" width="0.127" layer="21"/>
<wire x1="1.27" y1="-3.81" x2="-1.27" y2="-3.81" width="0.127" layer="21"/>
<wire x1="-1.27" y1="-3.81" x2="-1.27" y2="3.81" width="0.127" layer="21"/>
</package>
<package name="SDS011">
<pad name="P$1" x="0" y="3.81" drill="1" shape="square"/>
<pad name="P$2" x="0" y="1.27" drill="1" shape="square"/>
<pad name="P$3" x="0" y="-1.27" drill="1" shape="square"/>
<pad name="P$4" x="0" y="-3.81" drill="1" shape="square"/>
<wire x1="-1.27" y1="5.08" x2="1.27" y2="5.08" width="0.127" layer="21"/>
<wire x1="1.27" y1="5.08" x2="1.27" y2="-5.08" width="0.127" layer="21"/>
<wire x1="1.27" y1="-5.08" x2="-1.27" y2="-5.08" width="0.127" layer="21"/>
<wire x1="-1.27" y1="-5.08" x2="-1.27" y2="5.08" width="0.127" layer="21"/>
</package>
</packages>
<symbols>
<symbol name="LIS3DH">
<wire x1="-7.62" y1="12.7" x2="7.62" y2="12.7" width="0.254" layer="94"/>
<wire x1="7.62" y1="12.7" x2="7.62" y2="-10.16" width="0.254" layer="94"/>
<wire x1="7.62" y1="-10.16" x2="-7.62" y2="-10.16" width="0.254" layer="94"/>
<wire x1="-7.62" y1="-10.16" x2="-7.62" y2="12.7" width="0.254" layer="94"/>
<text x="-7.62" y="12.954" size="1.778" layer="95">&gt;NAME</text>
<text x="-7.62" y="-12.7" size="1.778" layer="96">&gt;VALUE</text>
<pin name="VIN" x="12.7" y="10.16" visible="pin" length="middle" direction="pwr" rot="R180"/>
<pin name="3VO" x="12.7" y="7.62" visible="pin" length="middle" direction="pwr" rot="R180"/>
<pin name="GND" x="12.7" y="5.08" visible="pin" length="middle" direction="pwr" rot="R180"/>
<pin name="SCL" x="12.7" y="2.54" visible="pin" length="middle" rot="R180"/>
<pin name="SDA" x="12.7" y="0" visible="pin" length="middle" rot="R180"/>
<pin name="SDO" x="12.7" y="-2.54" visible="pin" length="middle" rot="R180"/>
<pin name="CS" x="12.7" y="-5.08" visible="pin" length="middle" rot="R180"/>
<pin name="INT" x="12.7" y="-7.62" visible="pin" length="middle" rot="R180"/>
</symbol>
<symbol name="BN220">
<wire x1="-10.16" y1="7.62" x2="5.08" y2="7.62" width="0.254" layer="94"/>
<wire x1="5.08" y1="7.62" x2="5.08" y2="-5.08" width="0.254" layer="94"/>
<wire x1="5.08" y1="-5.08" x2="-10.16" y2="-5.08" width="0.254" layer="94"/>
<wire x1="-10.16" y1="-5.08" x2="-10.16" y2="7.62" width="0.254" layer="94"/>
<text x="-10.16" y="7.874" size="1.778" layer="95">&gt;NAME</text>
<text x="-10.16" y="-7.62" size="1.778" layer="96">&gt;VALUE</text>
<pin name="VIN" x="10.16" y="5.08" visible="pin" length="middle" direction="pwr" rot="R180"/>
<pin name="RX" x="10.16" y="2.54" visible="pin" length="middle" rot="R180"/>
<pin name="TX" x="10.16" y="0" visible="pin" length="middle" rot="R180"/>
<pin name="GND" x="10.16" y="-2.54" visible="pin" length="middle" direction="pwr" rot="R180"/>
</symbol>
<symbol name="BME280">
<wire x1="-7.62" y1="10.16" x2="7.62" y2="10.16" width="0.254" layer="94"/>
<wire x1="7.62" y1="10.16" x2="7.62" y2="-7.62" width="0.254" layer="94"/>
<wire x1="7.62" y1="-7.62" x2="-7.62" y2="-7.62" width="0.254" layer="94"/>
<wire x1="-7.62" y1="-7.62" x2="-7.62" y2="10.16" width="0.254" layer="94"/>
<text x="-7.62" y="10.414" size="1.778" layer="95">&gt;NAME</text>
<text x="-7.62" y="-10.16" size="1.778" layer="96">&gt;VALUE</text>
<pin name="VIN" x="12.7" y="7.62" visible="pin" length="middle" direction="pwr" rot="R180"/>
<pin name="GND" x="12.7" y="5.08" visible="pin" length="middle" direction="pwr" rot="R180"/>
<pin name="SCL" x="12.7" y="2.54" visible="pin" length="middle" rot="R180"/>
<pin name="SDA" x="12.7" y="0" visible="pin" length="middle" rot="R180"/>
<pin name="CSD" x="12.7" y="-2.54" visible="pin" length="middle" rot="R180"/>
<pin name="SDO" x="12.7" y="-5.08" visible="pin" length="middle" rot="R180"/>
</symbol>
<symbol name="ESP32T-CALL">
<pin name="NC" x="-25.4" y="22.86" visible="pin" length="middle"/>
<pin name="SVP" x="-25.4" y="20.32" visible="pin" length="middle"/>
<pin name="SVN" x="-25.4" y="17.78" visible="pin" length="middle"/>
<pin name="34" x="-25.4" y="15.24" visible="pin" length="middle"/>
<pin name="35" x="-25.4" y="12.7" visible="pin" length="middle"/>
<pin name="32" x="-25.4" y="10.16" visible="pin" length="middle"/>
<pin name="25" x="-25.4" y="5.08" visible="pin" length="middle"/>
<pin name="26" x="-25.4" y="2.54" visible="pin" length="middle"/>
<pin name="27" x="-25.4" y="0" visible="pin" length="middle"/>
<pin name="14" x="-25.4" y="-2.54" visible="pin" length="middle"/>
<pin name="12" x="-25.4" y="-5.08" visible="pin" length="middle"/>
<pin name="13" x="-25.4" y="-10.16" visible="pin" length="middle"/>
<pin name="SD2" x="-25.4" y="-12.7" visible="pin" length="middle"/>
<pin name="SD3" x="-25.4" y="-15.24" visible="pin" length="middle"/>
<pin name="CMD" x="-25.4" y="-17.78" visible="pin" length="middle"/>
<pin name="SPK+" x="-25.4" y="-22.86" visible="pin" length="middle"/>
<pin name="SPK-" x="-25.4" y="-25.4" visible="pin" length="middle"/>
<pin name="33" x="-25.4" y="7.62" visible="pin" length="middle"/>
<pin name="MIC+" x="25.4" y="-25.4" visible="pin" length="middle" rot="R180"/>
<pin name="MIC-" x="25.4" y="-22.86" visible="pin" length="middle" rot="R180"/>
<pin name="CLK" x="25.4" y="-20.32" visible="pin" length="middle" rot="R180"/>
<pin name="SD0" x="25.4" y="-17.78" visible="pin" length="middle" rot="R180"/>
<pin name="SD1" x="25.4" y="-15.24" visible="pin" length="middle" rot="R180"/>
<pin name="15" x="25.4" y="-12.7" visible="pin" length="middle" rot="R180"/>
<pin name="2" x="25.4" y="-10.16" visible="pin" length="middle" rot="R180"/>
<pin name="0" x="25.4" y="-7.62" visible="pin" length="middle" rot="R180"/>
<pin name="4" x="25.4" y="-5.08" visible="pin" length="middle" rot="R180"/>
<pin name="NC2" x="25.4" y="-2.54" visible="pin" length="middle" rot="R180"/>
<pin name="NC3" x="25.4" y="0" visible="pin" length="middle" rot="R180"/>
<pin name="5" x="25.4" y="2.54" visible="pin" length="middle" rot="R180"/>
<pin name="18" x="25.4" y="5.08" visible="pin" length="middle" rot="R180"/>
<pin name="19" x="25.4" y="7.62" visible="pin" length="middle" rot="R180"/>
<pin name="21" x="25.4" y="12.7" visible="pin" length="middle" rot="R180"/>
<pin name="RXD" x="25.4" y="15.24" visible="pin" length="middle" rot="R180"/>
<pin name="TXD" x="25.4" y="17.78" visible="pin" length="middle" rot="R180"/>
<pin name="22" x="25.4" y="20.32" visible="pin" length="middle" rot="R180"/>
<pin name="23" x="25.4" y="22.86" visible="pin" length="middle" rot="R180"/>
<wire x1="-20.32" y1="33.02" x2="20.32" y2="33.02" width="0.254" layer="94"/>
<wire x1="20.32" y1="33.02" x2="20.32" y2="-33.02" width="0.254" layer="94"/>
<wire x1="20.32" y1="-33.02" x2="-20.32" y2="-33.02" width="0.254" layer="94"/>
<wire x1="-20.32" y1="-33.02" x2="-20.32" y2="33.02" width="0.254" layer="94"/>
<text x="-20.32" y="33.274" size="1.27" layer="95">&gt;NAME</text>
<text x="-20.32" y="-35.56" size="1.27" layer="96">&gt;VALUE</text>
<pin name="ESP_3V3" x="-25.4" y="25.4" visible="pin" length="middle" direction="pwr"/>
<pin name="GND@1" x="-25.4" y="-7.62" visible="pin" length="middle" direction="pwr"/>
<pin name="GND@3" x="25.4" y="25.4" visible="pin" length="middle" direction="pwr" rot="R180"/>
<pin name="GND@2" x="25.4" y="10.16" visible="pin" length="middle" direction="pwr" rot="R180"/>
<pin name="ESP_5V" x="-25.4" y="-20.32" visible="pin" length="middle" direction="pwr"/>
</symbol>
<symbol name="MH-Z14A">
<wire x1="-7.62" y1="5.08" x2="7.62" y2="5.08" width="0.254" layer="94"/>
<wire x1="7.62" y1="5.08" x2="7.62" y2="-5.08" width="0.254" layer="94"/>
<wire x1="7.62" y1="-5.08" x2="-7.62" y2="-5.08" width="0.254" layer="94"/>
<wire x1="-7.62" y1="-5.08" x2="-7.62" y2="5.08" width="0.254" layer="94"/>
<text x="-7.62" y="5.334" size="1.778" layer="95">&gt;NAME</text>
<text x="-7.62" y="-7.62" size="1.778" layer="96">&gt;VALUE</text>
<pin name="VIN" x="12.7" y="2.54" visible="pin" length="middle" direction="pwr" rot="R180"/>
<pin name="GND" x="12.7" y="0" visible="pin" length="middle" direction="pwr" rot="R180"/>
<pin name="D" x="12.7" y="-2.54" visible="pin" length="middle" rot="R180"/>
</symbol>
<symbol name="SDS011">
<wire x1="-7.62" y1="7.62" x2="7.62" y2="7.62" width="0.254" layer="94"/>
<wire x1="7.62" y1="7.62" x2="7.62" y2="-5.08" width="0.254" layer="94"/>
<wire x1="7.62" y1="-5.08" x2="-7.62" y2="-5.08" width="0.254" layer="94"/>
<wire x1="-7.62" y1="-5.08" x2="-7.62" y2="7.62" width="0.254" layer="94"/>
<text x="-7.62" y="7.874" size="1.778" layer="95">&gt;NAME</text>
<text x="-7.62" y="-7.62" size="1.778" layer="96">&gt;VALUE</text>
<pin name="VIN" x="12.7" y="5.08" visible="pin" length="middle" direction="pwr" rot="R180"/>
<pin name="GND" x="12.7" y="2.54" visible="pin" length="middle" direction="pwr" rot="R180"/>
<pin name="PM10" x="12.7" y="0" visible="pin" length="middle" rot="R180"/>
<pin name="PM25" x="12.7" y="-2.54" visible="pin" length="middle" rot="R180"/>
</symbol>
</symbols>
<devicesets>
<deviceset name="LIS3DH">
<gates>
<gate name="G$1" symbol="LIS3DH" x="0" y="0"/>
</gates>
<devices>
<device name="" package="LIS3DH">
<connects>
<connect gate="G$1" pin="3VO" pad="P$2"/>
<connect gate="G$1" pin="CS" pad="P$7"/>
<connect gate="G$1" pin="GND" pad="P$3"/>
<connect gate="G$1" pin="INT" pad="P$8"/>
<connect gate="G$1" pin="SCL" pad="P$4"/>
<connect gate="G$1" pin="SDA" pad="P$5"/>
<connect gate="G$1" pin="SDO" pad="P$6"/>
<connect gate="G$1" pin="VIN" pad="P$1"/>
</connects>
<technologies>
<technology name=""/>
</technologies>
</device>
</devices>
</deviceset>
<deviceset name="BN220">
<gates>
<gate name="G$1" symbol="BN220" x="0" y="0"/>
</gates>
<devices>
<device name="" package="BN220">
<connects>
<connect gate="G$1" pin="GND" pad="P$4"/>
<connect gate="G$1" pin="RX" pad="P$2"/>
<connect gate="G$1" pin="TX" pad="P$3"/>
<connect gate="G$1" pin="VIN" pad="P$1"/>
</connects>
<technologies>
<technology name=""/>
</technologies>
</device>
</devices>
</deviceset>
<deviceset name="BME280">
<gates>
<gate name="G$1" symbol="BME280" x="0" y="0"/>
</gates>
<devices>
<device name="" package="BME280">
<connects>
<connect gate="G$1" pin="CSD" pad="P$5"/>
<connect gate="G$1" pin="GND" pad="P$2"/>
<connect gate="G$1" pin="SCL" pad="P$3"/>
<connect gate="G$1" pin="SDA" pad="P$4"/>
<connect gate="G$1" pin="SDO" pad="P$6"/>
<connect gate="G$1" pin="VIN" pad="P$1"/>
</connects>
<technologies>
<technology name=""/>
</technologies>
</device>
</devices>
</deviceset>
<deviceset name="ESP32T-CALL">
<gates>
<gate name="G$1" symbol="ESP32T-CALL" x="0" y="0"/>
</gates>
<devices>
<device name="" package="ESP32T-CALL">
<connects>
<connect gate="G$1" pin="0" pad="GPIO0"/>
<connect gate="G$1" pin="12" pad="GPIO12"/>
<connect gate="G$1" pin="13" pad="GPIO13"/>
<connect gate="G$1" pin="14" pad="GPIO14"/>
<connect gate="G$1" pin="15" pad="GPIO15"/>
<connect gate="G$1" pin="18" pad="GPIO18"/>
<connect gate="G$1" pin="19" pad="GPIO19"/>
<connect gate="G$1" pin="2" pad="GPIO2"/>
<connect gate="G$1" pin="21" pad="GPIO21"/>
<connect gate="G$1" pin="22" pad="GPIO22"/>
<connect gate="G$1" pin="23" pad="GPIO23"/>
<connect gate="G$1" pin="25" pad="GPIO25"/>
<connect gate="G$1" pin="26" pad="GPIO26"/>
<connect gate="G$1" pin="27" pad="GPIO27"/>
<connect gate="G$1" pin="32" pad="GPIO32"/>
<connect gate="G$1" pin="33" pad="GPIO33"/>
<connect gate="G$1" pin="34" pad="GPIO34"/>
<connect gate="G$1" pin="35" pad="GPIO35"/>
<connect gate="G$1" pin="4" pad="GPIO4"/>
<connect gate="G$1" pin="5" pad="GPIO5"/>
<connect gate="G$1" pin="CLK" pad="CLK"/>
<connect gate="G$1" pin="CMD" pad="CMD"/>
<connect gate="G$1" pin="ESP_3V3" pad="ESP32_3V3"/>
<connect gate="G$1" pin="ESP_5V" pad="ESP32_5V"/>
<connect gate="G$1" pin="GND@1" pad="GND"/>
<connect gate="G$1" pin="GND@2" pad="GND2"/>
<connect gate="G$1" pin="GND@3" pad="GND3"/>
<connect gate="G$1" pin="MIC+" pad="MIC+"/>
<connect gate="G$1" pin="MIC-" pad="MIC-"/>
<connect gate="G$1" pin="NC" pad="P$2"/>
<connect gate="G$1" pin="NC2" pad="NC2"/>
<connect gate="G$1" pin="NC3" pad="NC3"/>
<connect gate="G$1" pin="RXD" pad="RXD"/>
<connect gate="G$1" pin="SD0" pad="SD0"/>
<connect gate="G$1" pin="SD1" pad="SD1"/>
<connect gate="G$1" pin="SD2" pad="SD2"/>
<connect gate="G$1" pin="SD3" pad="SD3"/>
<connect gate="G$1" pin="SPK+" pad="SPK+"/>
<connect gate="G$1" pin="SPK-" pad="SPK-"/>
<connect gate="G$1" pin="SVN" pad="SVN"/>
<connect gate="G$1" pin="SVP" pad="SVP"/>
<connect gate="G$1" pin="TXD" pad="TXD"/>
</connects>
<technologies>
<technology name=""/>
</technologies>
</device>
</devices>
</deviceset>
<deviceset name="MH-Z14A">
<gates>
<gate name="G$1" symbol="MH-Z14A" x="0" y="0"/>
</gates>
<devices>
<device name="" package="MH-Z14A">
<connects>
<connect gate="G$1" pin="D" pad="P$3"/>
<connect gate="G$1" pin="GND" pad="P$2"/>
<connect gate="G$1" pin="VIN" pad="P$1"/>
</connects>
<technologies>
<technology name=""/>
</technologies>
</device>
</devices>
</deviceset>
<deviceset name="SDS011">
<gates>
<gate name="G$1" symbol="SDS011" x="0" y="0"/>
</gates>
<devices>
<device name="" package="SDS011">
<connects>
<connect gate="G$1" pin="GND" pad="P$2"/>
<connect gate="G$1" pin="PM10" pad="P$3"/>
<connect gate="G$1" pin="PM25" pad="P$4"/>
<connect gate="G$1" pin="VIN" pad="P$1"/>
</connects>
<technologies>
<technology name=""/>
</technologies>
</device>
</devices>
</deviceset>
</devicesets>
</library>
</libraries>
<attributes>
</attributes>
<variantdefs>
</variantdefs>
<classes>
<class number="0" name="default" width="0" drill="0">
</class>
</classes>
<parts>
<part name="U$2" library="Bikota" deviceset="LIS3DH" device=""/>
<part name="U$3" library="Bikota" deviceset="BN220" device=""/>
<part name="U$4" library="Bikota" deviceset="BME280" device=""/>
<part name="U$1" library="Bikota" deviceset="ESP32T-CALL" device=""/>
<part name="U$5" library="Bikota" deviceset="MH-Z14A" device=""/>
<part name="U$6" library="Bikota" deviceset="SDS011" device=""/>
</parts>
<sheets>
<sheet>
<plain>
</plain>
<instances>
<instance part="U$2" gate="G$1" x="5.08" y="76.2" smashed="yes">
<attribute name="NAME" x="-2.54" y="89.154" size="1.778" layer="95"/>
<attribute name="VALUE" x="-2.54" y="63.5" size="1.778" layer="96"/>
</instance>
<instance part="U$3" gate="G$1" x="7.62" y="33.02" smashed="yes">
<attribute name="NAME" x="-2.54" y="40.894" size="1.778" layer="95"/>
<attribute name="VALUE" x="-2.54" y="25.4" size="1.778" layer="96"/>
</instance>
<instance part="U$4" gate="G$1" x="215.9" y="81.28" smashed="yes" rot="R180">
<attribute name="NAME" x="223.52" y="70.866" size="1.778" layer="95" rot="R180"/>
<attribute name="VALUE" x="223.52" y="91.44" size="1.778" layer="96" rot="R180"/>
</instance>
<instance part="U$1" gate="G$1" x="114.3" y="55.88" smashed="yes">
<attribute name="NAME" x="93.98" y="89.154" size="1.27" layer="95"/>
<attribute name="VALUE" x="93.98" y="20.32" size="1.27" layer="96"/>
</instance>
<instance part="U$5" gate="G$1" x="215.9" y="53.34" smashed="yes" rot="R180">
<attribute name="NAME" x="223.52" y="48.006" size="1.778" layer="95" rot="R180"/>
<attribute name="VALUE" x="223.52" y="60.96" size="1.778" layer="96" rot="R180"/>
</instance>
<instance part="U$6" gate="G$1" x="215.9" y="30.48" smashed="yes" rot="R180">
<attribute name="NAME" x="223.52" y="22.606" size="1.778" layer="95" rot="R180"/>
<attribute name="VALUE" x="223.52" y="38.1" size="1.778" layer="96" rot="R180"/>
</instance>
</instances>
<busses>
</busses>
<nets>
<net name="ACC_INT" class="0">
<segment>
<wire x1="17.78" y1="68.58" x2="27.94" y2="68.58" width="0.1524" layer="91"/>
<label x="27.94" y="68.58" size="1.778" layer="95"/>
<pinref part="U$2" gate="G$1" pin="INT"/>
</segment>
<segment>
<wire x1="88.9" y1="53.34" x2="66.04" y2="53.34" width="0.1524" layer="91"/>
<label x="66.04" y="53.34" size="1.778" layer="95"/>
<pinref part="U$1" gate="G$1" pin="14"/>
</segment>
</net>
<net name="ESP32_5V" class="0">
<segment>
<wire x1="17.78" y1="86.36" x2="27.94" y2="86.36" width="0.1524" layer="91"/>
<label x="27.94" y="86.36" size="1.778" layer="95"/>
<pinref part="U$2" gate="G$1" pin="VIN"/>
</segment>
<segment>
<wire x1="88.9" y1="35.56" x2="66.04" y2="35.56" width="0.1524" layer="91"/>
<label x="66.04" y="35.56" size="1.778" layer="95"/>
<pinref part="U$1" gate="G$1" pin="ESP_5V"/>
</segment>
</net>
<net name="GND" class="0">
<segment>
<wire x1="88.9" y1="48.26" x2="66.04" y2="48.26" width="0.1524" layer="91"/>
<label x="66.04" y="48.26" size="1.778" layer="95"/>
<pinref part="U$1" gate="G$1" pin="GND@1"/>
</segment>
<segment>
<wire x1="17.78" y1="81.28" x2="27.94" y2="81.28" width="0.1524" layer="91"/>
<label x="27.94" y="81.28" size="1.778" layer="95"/>
<pinref part="U$2" gate="G$1" pin="GND"/>
</segment>
</net>
<net name="SDA" class="0">
<segment>
<wire x1="139.7" y1="68.58" x2="154.94" y2="68.58" width="0.1524" layer="91"/>
<label x="154.94" y="68.58" size="1.778" layer="95"/>
<pinref part="U$1" gate="G$1" pin="21"/>
</segment>
<segment>
<wire x1="17.78" y1="76.2" x2="27.94" y2="76.2" width="0.1524" layer="91"/>
<label x="27.94" y="76.2" size="1.778" layer="95"/>
<pinref part="U$2" gate="G$1" pin="SDA"/>
</segment>
<segment>
<pinref part="U$4" gate="G$1" pin="SDA"/>
<wire x1="203.2" y1="81.28" x2="190.5" y2="81.28" width="0.1524" layer="91"/>
<label x="190.5" y="81.28" size="1.778" layer="95"/>
</segment>
</net>
<net name="SCL" class="0">
<segment>
<wire x1="139.7" y1="76.2" x2="154.94" y2="76.2" width="0.1524" layer="91"/>
<label x="154.94" y="76.2" size="1.778" layer="95"/>
<pinref part="U$1" gate="G$1" pin="22"/>
</segment>
<segment>
<wire x1="17.78" y1="78.74" x2="27.94" y2="78.74" width="0.1524" layer="91"/>
<label x="27.94" y="78.74" size="1.778" layer="95"/>
<pinref part="U$2" gate="G$1" pin="SCL"/>
</segment>
<segment>
<pinref part="U$4" gate="G$1" pin="SCL"/>
<wire x1="203.2" y1="78.74" x2="190.5" y2="78.74" width="0.1524" layer="91"/>
<label x="190.5" y="78.74" size="1.778" layer="95"/>
</segment>
</net>
<net name="N$1" class="0">
<segment>
<wire x1="17.78" y1="38.1" x2="27.94" y2="38.1" width="0.1524" layer="91"/>
<label x="27.94" y="38.1" size="1.778" layer="95"/>
<pinref part="U$3" gate="G$1" pin="VIN"/>
</segment>
</net>
<net name="GPS_RX" class="0">
<segment>
<wire x1="17.78" y1="35.56" x2="27.94" y2="35.56" width="0.1524" layer="91"/>
<label x="27.94" y="35.56" size="1.778" layer="95"/>
<pinref part="U$3" gate="G$1" pin="RX"/>
</segment>
</net>
<net name="GPS_TX" class="0">
<segment>
<wire x1="17.78" y1="33.02" x2="27.94" y2="33.02" width="0.1524" layer="91"/>
<label x="27.94" y="33.02" size="1.778" layer="95"/>
<pinref part="U$3" gate="G$1" pin="TX"/>
</segment>
<segment>
<pinref part="U$1" gate="G$1" pin="35"/>
<wire x1="88.9" y1="68.58" x2="66.04" y2="68.58" width="0.1524" layer="91"/>
<label x="66.04" y="68.58" size="1.778" layer="95"/>
</segment>
</net>
<net name="N$4" class="0">
<segment>
<wire x1="17.78" y1="30.48" x2="27.94" y2="30.48" width="0.1524" layer="91"/>
<label x="27.94" y="30.48" size="1.778" layer="95"/>
<pinref part="U$3" gate="G$1" pin="GND"/>
</segment>
</net>
<net name="N$9" class="0">
<segment>
<pinref part="U$4" gate="G$1" pin="GND"/>
<wire x1="203.2" y1="76.2" x2="190.5" y2="76.2" width="0.1524" layer="91"/>
<label x="190.5" y="76.2" size="1.778" layer="95"/>
</segment>
</net>
<net name="N$10" class="0">
<segment>
<pinref part="U$4" gate="G$1" pin="VIN"/>
<wire x1="203.2" y1="73.66" x2="190.5" y2="73.66" width="0.1524" layer="91"/>
<label x="190.5" y="73.66" size="1.778" layer="95"/>
</segment>
</net>
<net name="SVP" class="0">
<segment>
<pinref part="U$5" gate="G$1" pin="D"/>
<wire x1="203.2" y1="55.88" x2="190.5" y2="55.88" width="0.1524" layer="91"/>
<label x="190.5" y="55.88" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="U$1" gate="G$1" pin="SVP"/>
<wire x1="88.9" y1="76.2" x2="66.04" y2="76.2" width="0.1524" layer="91"/>
<label x="66.04" y="76.2" size="1.778" layer="95"/>
</segment>
</net>
<net name="N$12" class="0">
<segment>
<pinref part="U$5" gate="G$1" pin="GND"/>
<wire x1="203.2" y1="53.34" x2="190.5" y2="53.34" width="0.1524" layer="91"/>
<label x="190.5" y="53.34" size="1.778" layer="95"/>
</segment>
</net>
<net name="N$13" class="0">
<segment>
<pinref part="U$5" gate="G$1" pin="VIN"/>
<wire x1="203.2" y1="50.8" x2="190.5" y2="50.8" width="0.1524" layer="91"/>
<label x="190.5" y="50.8" size="1.778" layer="95"/>
</segment>
</net>
<net name="PM25" class="0">
<segment>
<pinref part="U$6" gate="G$1" pin="PM25"/>
<wire x1="203.2" y1="33.02" x2="190.5" y2="33.02" width="0.1524" layer="91"/>
<label x="190.5" y="33.02" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="U$1" gate="G$1" pin="19"/>
<wire x1="139.7" y1="63.5" x2="154.94" y2="63.5" width="0.1524" layer="91"/>
<label x="154.94" y="63.5" size="1.778" layer="95"/>
</segment>
</net>
<net name="PM10" class="0">
<segment>
<pinref part="U$6" gate="G$1" pin="PM10"/>
<wire x1="203.2" y1="30.48" x2="190.5" y2="30.48" width="0.1524" layer="91"/>
<label x="190.5" y="30.48" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="U$1" gate="G$1" pin="18"/>
<wire x1="139.7" y1="60.96" x2="154.94" y2="60.96" width="0.1524" layer="91"/>
<label x="154.94" y="60.96" size="1.778" layer="95"/>
</segment>
</net>
<net name="N$8" class="0">
<segment>
<pinref part="U$6" gate="G$1" pin="VIN"/>
<wire x1="203.2" y1="25.4" x2="190.5" y2="25.4" width="0.1524" layer="91"/>
<label x="190.5" y="25.4" size="1.778" layer="95"/>
</segment>
</net>
<net name="N$7" class="0">
<segment>
<pinref part="U$6" gate="G$1" pin="GND"/>
<wire x1="203.2" y1="27.94" x2="190.5" y2="27.94" width="0.1524" layer="91"/>
<label x="190.5" y="27.94" size="1.778" layer="95"/>
</segment>
</net>
</nets>
</sheet>
</sheets>
</schematic>
</drawing>
</eagle>

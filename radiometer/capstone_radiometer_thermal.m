mb=0.025;  %wavelength (in m) 0.05 at 6GHz, 0.025 at 12GHz
B=100000000; %radiometer bandwidth (guessed 100MHz)
eta=377;     %intrinsic impedance of free space (constant)
k=1.38E-23;  %Boltzmann's constant
K=(lamb^2)/(k*eta*B);   %a scale factor to convert (V/m)^2 to Kelvins
Ep=0.000001;   %electric field in volts (likely will not even get close to a micro-volt)
Tb=K*(abs(Ep)^2);   %brightness temperature that the radiometer is measuring

%T antenna is about equal to Tb if the antenna is perfectly efficient.
%if lamb = 0.025 and Ep = 1 micro-volt, Tb=0.0012 Kelvin.
%Tb and consequently T antenna is negligible from the radiometer.

// preamble ////////////////////////////////////////////////////////////////////
#include <boost/python.hpp>
#include <cmath>
namespace py = boost::python;
/*******************************************************************************
 c++ module 
*******************************************************************************/
////////////////////////////////////////////////////////////////////////////////
// class vector ////////////////////////////////////////////////////////////////
/* simple personalized vector
 * 
 */
class vec{
private:
	double x;
	double y;
public:
	// constructor
	vec( double x, double y) : x{x}, y{y} {}
	// methods
	double get_x(){ return x; }
	double get_y(){ return y; }
	double get_length(){ return std::sqrt( x*x + y*y ); }
	double get_angle(){ return std::atan(y/x); }
	py::list get_vec();
	vec& operator= ( vec v);
	vec operator+( vec v);
	vec operator*( vec v);
	void set_vec( double length, double angle );
};
//  method for python lists
py::list vec::get_vec(){
	py::list p;
	p.append(get_x());
	p.append(get_y());
	return p;
}
// methods to simplify expresions
vec& vec::operator= ( vec v){
	x = v.get_x();
	y = v.get_y();
	return *this;
}

vec vec::operator+ ( vec v){
	return vec((v.get_x() + this->get_x()) , (v.get_y() + this->get_y())); 
}

vec vec::operator* ( vec v){
	return vec((v.get_x() * this->get_x()) , (v.get_y() * this->get_y()));
}

vec operator*(double a, vec v){
	return vec( (v.get_x())*a , (v.get_y())*a );
}

void vec::set_vec( double length, double angle){
	*this = vec( length * std::cos(angle) , length * std::sin(angle));
}
////////////////////////////////////////////////////////////////////////////////
// class external //////////////////////////////////////////////////////////////
/* contain info about: ait density, speed of wind and gravitation
 */
class external{
private:
	double density;
	vec velocity;
	vec gravitation;
public:
	// constructor
	external( double d, vec v , vec g ) 
		: density{d} , velocity{v} , gravitation{g} { }
	// methods
	double get_density(){ return density; }
	vec get_wind(){ return velocity; }
	vec get_gravitation(){ return gravitation; }
};
////////////////////////////////////////////////////////////////////////////////
// class bullet ////////////////////////////////////////////////////////////////
/* bullet - class that contains key methods 
 * 
 */
class bullet{
private:
	double mass;
	vec position;
	vec velocity;
	double drag_cs;
	
public:
	// constructor
	bullet(double m, vec p, vec v, double c)
		: mass{m}, position{p}, velocity{v}, drag_cs{c}  { }
	// methods
	double get_mass(){ return mass; }
	vec get_position(){ return position; }
	vec get_velocity(){ return velocity; }
	void next_v( external conditions , double time_step );
	void next_point( external conditions, double time_step);
};
// we assume that air drag is proportional to square of velocity
void bullet::next_v( external conditions, double time_step){
	// calculate of drag value
	// R = C*S*rho*v^2 /2
	vec drag_force(0,0);
	vec v_r = conditions.get_wind() + velocity; // v
	double df_length = v_r.get_length() * v_r.get_length();	// |v|^2
	df_length *= (conditions.get_density() / 2.) * drag_cs; // C*S*rho*v^2 /2
	drag_force.set_vec(df_length, v_r.get_angle() + 3.14159265); 
	velocity = velocity +										// from II N. p.
		mass * time_step * (drag_force + conditions.get_gravitation());
}

void bullet::next_point( external conditions, double time_step){
	position = position + time_step * velocity;
	next_v( conditions, time_step);
}
////////////////////////////////////////////////////////////////////////////////
// funkcja symulujaca rzut /////////////////////////////////////////////////////
class simulation{
private:
	// axis
	double x_max, y_max, x_min, y_min;
	//  python list 
	py::list out;
public:
	simulation( bullet bull, external conditions, double time_step);
	py::list get_out(){ return out; }
	double get_x_max(){ return x_max; }
	double get_y_max(){ return y_max; }
	double get_x_min(){ return x_min; }
	double get_y_min(){ return y_min; }
};

simulation::simulation( bullet bull, external conditions ,  double time_step){
	x_max = x_min = bull.get_position().get_x();
	y_max = y_min = bull.get_position().get_y();
	
	py::list out_x, out_y;
	
	long t = 0;
	long t_safe = 50000;
	double X, Y;
	
	while( bull.get_position().get_y() > -1){
		if( t > t_safe ) break;
		++t;

		X = bull.get_position().get_x();
		Y = bull.get_position().get_y();
		out_x.append( X );
		out_y.append( Y );

		bull.next_point( conditions, time_step);
	}
	// wpisywanie do listy wyjsciowej
	out.append( out_x );
	out.append( out_y );
}
/*******************************************************************************
 boost module 
*******************************************************************************/

using namespace py;

BOOST_PYTHON_MODULE(sim)
{
	class_<vec>("vector", init<double, double>())
		.def("read_y", &vec::get_y )
		.def("read_x", &vec::get_x )
		.def("read_length", &vec::get_length )
		.def("read_vector" , &vec::get_vec )
		;
		
	class_<external>("external", init<double, vec, vec>())
		;
		
	class_<bullet>("bullet", init<double, vec, vec, double>())
		.def("read_mass", &bullet::get_mass )
		.def("read_position", &bullet::get_position )
		.def("read_velocity", &bullet::get_velocity )
		.def( "next_point", &bullet::next_point )
		;
		
	class_<simulation>("simulation", init< bullet, external, double>())
		.def("read_x_max", &simulation::get_x_max )
		.def("read_x_min", &simulation::get_x_min )
		.def("read_y_max", &simulation::get_y_max )
		.def("read_y_min", &simulation::get_y_min )
		.def("read_out", &simulation::get_out )
		;
}

////////////////////////////////////////////////////////////////////////////////

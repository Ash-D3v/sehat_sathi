import googlemaps
from typing import Dict, List, Tuple
import logging
from config.settings import Config

class LocationService:
    def __init__(self):
        self.config = Config()
        self.logger = logging.getLogger(__name__)
        
        # Initialize Google Maps client
        self.gmaps = googlemaps.Client(key=self.config.GOOGLE_MAPS_API_KEY)
        
        # Emergency contacts for Indian cities
        self.emergency_contacts = {
            'mumbai': ['+91-22-24177777', '+91-22-24171111'],
            'delhi': ['+91-11-23221122', '+91-11-23223344'],
            'chennai': ['+91-44-28411111', '+91-44-28522222'],
            'kolkata': ['+91-33-22143526', '+91-33-22876543'],
            'bangalore': ['+91-80-22344444', '+91-80-22555555']
        }

    def find_nearby_hospitals(self, user_location: Dict, severity: str) -> List[Dict]:
        """Find nearby hospitals based on severity"""
        try:
            # Extract coordinates
            if 'lat' in user_location and 'lng' in user_location:
                location = (user_location['lat'], user_location['lng'])
            else:
                self.logger.error("Invalid location format")
                return []

            # Determine search parameters based on severity
            if severity == "high":
                search_types = ['hospital', 'emergency_room']
                radius = 10000  # 10km for emergencies
            elif severity == "medium":
                search_types = ['hospital', 'clinic']
                radius = 5000   # 5km for medium severity
            else:
                search_types = ['clinic', 'pharmacy']
                radius = 3000   # 3km for low severity

            all_places = []
            
            for search_type in search_types:
                try:
                    places_result = self.gmaps.places_nearby(
                        location=location,
                        radius=radius,
                        type=search_type,
                        language='en'
                    )
                    all_places.extend(places_result.get('results', []))
                except Exception as e:
                    self.logger.error(f"Error searching for {search_type}: {e}")

            # Process and rank results
            hospitals = []
            for place in all_places[:10]:  # Limit to top 10
                try:
                    hospital_info = self._process_hospital_info(place, location)
                    if hospital_info:
                        hospitals.append(hospital_info)
                except Exception as e:
                    self.logger.error(f"Error processing hospital info: {e}")

            # Sort by rating and distance
            hospitals.sort(key=lambda x: (-x.get('rating', 0), x.get('distance', float('inf'))))
            
            return hospitals[:5]  # Return top 5

        except Exception as e:
            self.logger.error(f"Error finding hospitals: {e}")
            return []

    def _process_hospital_info(self, place: Dict, user_location: Tuple) -> Dict:
        """Process individual hospital information"""
        try:
            place_location = (
                place['geometry']['location']['lat'],
                place['geometry']['location']['lng']
            )
            
            # Calculate distance
            distance = self._calculate_distance(user_location, place_location)
            
            # Get additional details
            place_details = self._get_place_details(place['place_id'])
            
            hospital_info = {
                'name': place.get('name', 'Unknown Hospital'),
                'address': place.get('vicinity', 'Address not available'),
                'rating': place.get('rating', 0),
                'distance': distance,
                'distance_text': f"{distance:.1f} km",
                'place_id': place['place_id'],
                'location': place_location,
                'phone': place_details.get('phone', 'Not available'),
                'website': place_details.get('website', ''),
                'opening_hours': place_details.get('opening_hours', {}),
                'types': place.get('types', [])
            }
            
            # Add emergency flag for high-priority places
            if any(t in place.get('types', []) for t in ['emergency_room', 'hospital']):
                hospital_info['is_emergency'] = True
            else:
                hospital_info['is_emergency'] = False
                
            return hospital_info
            
        except Exception as e:
            self.logger.error(f"Error processing hospital: {e}")
            return None

    def _get_place_details(self, place_id: str) -> Dict:
        """Get detailed information about a place"""
        try:
            fields = ['phone_number', 'website', 'opening_hours']
            details = self.gmaps.place(place_id=place_id, fields=fields)
            return details.get('result', {})
        except Exception as e:
            self.logger.error(f"Error getting place details: {e}")
            return {}

    def _calculate_distance(self, location1: Tuple, location2: Tuple) -> float:
        """Calculate distance between two coordinates in kilometers"""
        try:
            # Use Google Maps Distance Matrix API for accurate results
            result = self.gmaps.distance_matrix(
                origins=[location1],
                destinations=[location2],
                mode="driving",
                units="metric"
            )
            
            distance_info = result['rows'][0]['elements'][0]
            if distance_info['status'] == 'OK':
                # Extract distance in kilometers
                distance_text = distance_info['distance']['text']
                if 'km' in distance_text:
                    return float(distance_text.replace(' km', ''))
                elif 'm' in distance_text:
                    return float(distance_text.replace(' m', '')) / 1000
            
            # Fallback to haversine formula
            return self._haversine_distance(location1, location2)
            
        except Exception as e:
            self.logger.error(f"Error calculating distance: {e}")
            return self._haversine_distance(location1, location2)

    def _haversine_distance(self, location1: Tuple, location2: Tuple) -> float:
        """Calculate distance using haversine formula"""
        import math
        
        lat1, lon1 = location1
        lat2, lon2 = location2
        
        # Convert to radians
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        
        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        # Earth's radius in kilometers
        r = 6371
        
        return c * r

    def get_emergency_contacts(self, city: str) -> List[str]:
        """Get emergency contacts for a city"""
        city_lower = city.lower()
        return self.emergency_contacts.get(city_lower, ['108'])  # 108 is India's emergency number

    def get_directions(self, origin: Dict, destination: Dict) -> Dict:
        """Get directions between two points"""
        try:
            directions = self.gmaps.directions(
                origin=(origin['lat'], origin['lng']),
                destination=(destination['lat'], destination['lng']),
                mode="driving"
            )
            
            if directions:
                route = directions[0]
                return {
                    'duration': route['legs'][0]['duration']['text'],
                    'distance': route['legs'][0]['distance']['text'],
                    'steps': [step['html_instructions'] for step in route['legs'][0]['steps'][:5]]  # First 5 steps
                }
            
        except Exception as e:
            self.logger.error(f"Error getting directions: {e}")
        
        return {}
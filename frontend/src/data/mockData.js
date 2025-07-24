// Mock data for symptom checker
export const SYMPTOMS_DATABASE = {
  // Respiratory symptoms
  'cough': ['common cold', 'flu', 'bronchitis', 'pneumonia', 'covid-19'],
  'fever': ['flu', 'infection', 'covid-19', 'malaria', 'typhoid'],
  'shortness of breath': ['asthma', 'pneumonia', 'heart attack', 'covid-19'],
  'chest pain': ['heart attack', 'angina', 'pneumonia', 'muscle strain'],
  
  // Gastrointestinal symptoms
  'stomach pain': ['gastritis', 'appendicitis', 'food poisoning', 'ulcer'],
  'nausea': ['food poisoning', 'gastritis', 'pregnancy', 'migraine'],
  'vomiting': ['food poisoning', 'gastritis', 'appendicitis', 'migraine'],
  'diarrhea': ['food poisoning', 'gastroenteritis', 'ibs', 'infection'],
  
  // Neurological symptoms
  'headache': ['tension headache', 'migraine', 'sinusitis', 'hypertension'],
  'dizziness': ['vertigo', 'low blood pressure', 'dehydration', 'anemia'],
  'confusion': ['stroke', 'dehydration', 'infection', 'diabetes'],
  
  // General symptoms
  'fatigue': ['anemia', 'diabetes', 'thyroid disorder', 'depression'],
  'body ache': ['flu', 'viral infection', 'fibromyalgia', 'arthritis'],
  'sore throat': ['common cold', 'strep throat', 'flu', 'tonsillitis']
};

export const DISEASES_DATABASE = {
  'common cold': {
    severity: 'low',
    description: 'A viral infection of the upper respiratory tract',
    symptoms: ['runny nose', 'sneezing', 'mild cough', 'sore throat'],
    treatment: 'Rest, fluids, and over-the-counter medications',
    duration: '7-10 days',
    urgency: 'self-care'
  },
  'flu': {
    severity: 'medium',
    description: 'Influenza viral infection',
    symptoms: ['fever', 'body ache', 'fatigue', 'cough'],
    treatment: 'Rest, antiviral medications if prescribed, fluids',
    duration: '1-2 weeks',
    urgency: 'doctor-consultation'
  },
  'pneumonia': {
    severity: 'high',
    description: 'Infection that inflames air sacs in lungs',
    symptoms: ['fever', 'cough', 'shortness of breath', 'chest pain'],
    treatment: 'Antibiotics, hospitalization may be required',
    duration: '2-3 weeks',
    urgency: 'immediate-medical-attention'
  },
  'heart attack': {
    severity: 'critical',
    description: 'Blockage of blood flow to the heart muscle',
    symptoms: ['severe chest pain', 'shortness of breath', 'nausea', 'sweating'],
    treatment: 'Emergency medical intervention required',
    duration: 'immediate',
    urgency: 'emergency'
  },
  'appendicitis': {
    severity: 'high',
    description: 'Inflammation of the appendix',
    symptoms: ['severe stomach pain', 'nausea', 'vomiting', 'fever'],
    treatment: 'Surgical removal of appendix',
    duration: 'immediate',
    urgency: 'emergency'
  },
  'gastritis': {
    severity: 'medium',
    description: 'Inflammation of the stomach lining',
    symptoms: ['stomach pain', 'nausea', 'bloating', 'loss of appetite'],
    treatment: 'Antacids, dietary changes, avoid spicy foods',
    duration: '1-2 weeks',
    urgency: 'doctor-consultation'
  },
  'migraine': {
    severity: 'medium',
    description: 'Severe recurring headache',
    symptoms: ['severe headache', 'nausea', 'sensitivity to light', 'vomiting'],
    treatment: 'Pain relievers, rest in dark room, prescribed medications',
    duration: '4-72 hours',
    urgency: 'doctor-consultation'
  },
  'hypertension': {
    severity: 'medium',
    description: 'High blood pressure',
    symptoms: ['headache', 'dizziness', 'chest pain', 'shortness of breath'],
    treatment: 'Lifestyle changes, blood pressure medications',
    duration: 'chronic condition',
    urgency: 'doctor-consultation'
  }
};

export const HOSPITALS_DATABASE = [
  {
    id: 1,
    name: 'City General Hospital',
    address: '123 Main Street, Downtown',
    phone: '+91-9876543210',
    specialties: ['Emergency', 'Cardiology', 'General Medicine'],
    distance: '2.5 km',
    rating: 4.5,
    emergency: true,
    coordinates: { lat: 28.6139, lng: 77.2090 }
  },
  {
    id: 2,
    name: 'Metro Medical Center',
    address: '456 Health Avenue, Central City',
    phone: '+91-9876543211',
    specialties: ['Internal Medicine', 'Surgery', 'Pediatrics'],
    distance: '3.2 km',
    rating: 4.3,
    emergency: true,
    coordinates: { lat: 28.6129, lng: 77.2095 }
  },
  {
    id: 3,
    name: 'Sunrise Clinic',
    address: '789 Wellness Road, Suburb',
    phone: '+91-9876543212',
    specialties: ['General Practice', 'Family Medicine'],
    distance: '1.8 km',
    rating: 4.1,
    emergency: false,
    coordinates: { lat: 28.6149, lng: 77.2085 }
  },
  {
    id: 4,
    name: 'Heart Care Specialty Hospital',
    address: '321 Cardiac Lane, Medical District',
    phone: '+91-9876543213',
    specialties: ['Cardiology', 'Cardiac Surgery', 'Emergency'],
    distance: '4.1 km',
    rating: 4.7,
    emergency: true,
    coordinates: { lat: 28.6119, lng: 77.2100 }
  }
];

export const DOCTORS_DATABASE = [
  {
    id: 1,
    name: 'Dr. Rajesh Kumar',
    specialty: 'General Medicine',
    hospital: 'City General Hospital',
    phone: '+91-9876543220',
    experience: '15 years',
    rating: 4.6,
    availability: 'Mon-Sat 9AM-6PM'
  },
  {
    id: 2,
    name: 'Dr. Priya Sharma',
    specialty: 'Cardiology',
    hospital: 'Heart Care Specialty Hospital',
    phone: '+91-9876543221',
    experience: '12 years',
    rating: 4.8,
    availability: 'Mon-Fri 10AM-5PM'
  },
  {
    id: 3,
    name: 'Dr. Amit Patel',
    specialty: 'Emergency Medicine',
    hospital: 'Metro Medical Center',
    phone: '+91-9876543222',
    experience: '10 years',
    rating: 4.4,
    availability: '24/7 Emergency'
  },
  {
    id: 4,
    name: 'Dr. Sunita Gupta',
    specialty: 'Internal Medicine',
    hospital: 'Sunrise Clinic',
    phone: '+91-9876543223',
    experience: '8 years',
    rating: 4.2,
    availability: 'Tue-Sun 11AM-7PM'
  }
];

export const EMERGENCY_CONTACTS = {
  ambulance: '108',
  police: '100',
  fire: '101',
  women_helpline: '1091',
  child_helpline: '1098'
};
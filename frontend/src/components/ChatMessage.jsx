import React from 'react';
import { MapPin, Phone, Star, Clock, User, AlertTriangle } from 'lucide-react';

const ChatMessage = ({ message, isBot }) => {
  if (!isBot) {
    return (
      <div className="flex justify-end mb-4">
        <div className="bg-blue-500 text-white rounded-lg rounded-br-sm px-4 py-2 max-w-xs lg:max-w-md">
          {message}
        </div>
      </div>
    );
  }

  // Bot message with analysis results
  return (
    <div className="flex justify-start mb-4">
      <div className="bg-gray-100 text-gray-800 rounded-lg rounded-bl-sm px-4 py-3 max-w-xs lg:max-w-2xl">
        {typeof message === 'string' ? (
          <p>{message}</p>
        ) : (
          <BotAnalysisMessage analysis={message} />
        )}
      </div>
    </div>
  );
};

const BotAnalysisMessage = ({ analysis }) => {
  const { topDisease, recommendations, severity, confidence, detectedSymptoms } = analysis;

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'low': return 'text-green-600 bg-green-100';
      case 'medium': return 'text-yellow-600 bg-yellow-100';
      case 'high': return 'text-orange-600 bg-orange-100';
      case 'critical': return 'text-red-600 bg-red-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  const getSeverityIcon = (severity) => {
    if (severity === 'critical' || severity === 'high') {
      return <AlertTriangle className="w-4 h-4" />;
    }
    return null;
  };

  return (
    <div className="space-y-4">
      {/* Detected Symptoms */}
      <div>
        <h4 className="font-semibold text-sm mb-2">Detected Symptoms:</h4>
        <div className="flex flex-wrap gap-1">
          {detectedSymptoms.map((symptom, index) => (
            <span key={index} className="bg-blue-100 text-blue-800 px-2 py-1 rounded-full text-xs">
              {symptom}
            </span>
          ))}
        </div>
      </div>

      {/* Disease Prediction */}
      <div>
        <h4 className="font-semibold text-sm mb-2">Possible Condition:</h4>
        <div className="bg-white rounded-lg p-3 border">
          <div className="flex items-center justify-between mb-2">
            <h5 className="font-medium capitalize">{topDisease.name}</h5>
            <div className={`flex items-center gap-1 px-2 py-1 rounded-full text-xs ${getSeverityColor(severity)}`}>
              {getSeverityIcon(severity)}
              <span className="capitalize">{severity}</span>
            </div>
          </div>
          <p className="text-sm text-gray-600 mb-2">{topDisease.description}</p>
          <p className="text-xs text-gray-500">Confidence: {Math.round(confidence)}%</p>
        </div>
      </div>

      {/* Recommendations */}
      <div>
        <h4 className="font-semibold text-sm mb-2">Recommendations:</h4>
        <div className="bg-white rounded-lg p-3 border">
          <div className={`flex items-center gap-2 mb-2 ${severity === 'critical' ? 'text-red-600' : ''}`}>
            {getSeverityIcon(severity)}
            <span className="font-medium">{recommendations.action}</span>
          </div>
          <p className="text-sm text-gray-600 mb-2">{recommendations.message}</p>
          <div className="text-sm">
            <p><strong>Treatment:</strong> {recommendations.treatment}</p>
            <p><strong>Expected Duration:</strong> {recommendations.duration}</p>
          </div>
        </div>
      </div>

      {/* Emergency Alert */}
      {severity === 'critical' && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-3">
          <div className="flex items-center gap-2 text-red-600 mb-2">
            <AlertTriangle className="w-5 h-5" />
            <span className="font-bold">MEDICAL EMERGENCY</span>
          </div>
          <p className="text-sm text-red-700 mb-2">
            Call emergency services immediately: <strong>108</strong>
          </p>
        </div>
      )}

      {/* Hospitals */}
      {recommendations.hospitals && recommendations.hospitals.length > 0 && (
        <div>
          <h4 className="font-semibold text-sm mb-2">
            {severity === 'critical' || severity === 'high' ? 'Nearest Emergency Hospitals:' : 'Recommended Healthcare Facilities:'}
          </h4>
          <div className="space-y-2">
            {recommendations.hospitals.map((hospital, index) => (
              <HospitalCard key={index} hospital={hospital} />
            ))}
          </div>
        </div>
      )}

      {/* Doctors */}
      {recommendations.doctors && recommendations.doctors.length > 0 && (
        <div>
          <h4 className="font-semibold text-sm mb-2">Recommended Doctors:</h4>
          <div className="space-y-2">
            {recommendations.doctors.map((doctor, index) => (
              <DoctorCard key={index} doctor={doctor} />
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

const HospitalCard = ({ hospital }) => {
  const generateMapUrl = () => {
    const { lat, lng } = hospital.coordinates;
    return `https://www.google.com/maps/search/?api=1&query=${lat},${lng}&query_place_id=${hospital.name}`;
  };

  return (
    <div className="bg-white rounded-lg p-3 border border-gray-200">
      <div className="flex items-start justify-between mb-2">
        <div>
          <h5 className="font-medium text-sm">{hospital.name}</h5>
          <div className="flex items-center gap-1 text-xs text-gray-500">
            <Star className="w-3 h-3 fill-yellow-400 text-yellow-400" />
            <span>{hospital.rating}</span>
            <span>•</span>
            <span>{hospital.distance}</span>
          </div>
        </div>
        {hospital.emergency && (
          <span className="bg-red-100 text-red-600 px-2 py-1 rounded-full text-xs font-medium">
            Emergency
          </span>
        )}
      </div>
      
      <p className="text-xs text-gray-600 mb-2">{hospital.address}</p>
      
      <div className="flex flex-wrap gap-1 mb-2">
        {hospital.specialties.map((specialty, index) => (
          <span key={index} className="bg-blue-50 text-blue-600 px-2 py-1 rounded text-xs">
            {specialty}
          </span>
        ))}
      </div>
      
      <div className="flex gap-2">
        <a
          href={`tel:${hospital.phone}`}
          className="flex items-center gap-1 bg-green-500 text-white px-3 py-1 rounded text-xs hover:bg-green-600 transition-colors"
        >
          <Phone className="w-3 h-3" />
          Call
        </a>
        <a
          href={generateMapUrl()}
          target="_blank"
          rel="noopener noreferrer"
          className="flex items-center gap-1 bg-blue-500 text-white px-3 py-1 rounded text-xs hover:bg-blue-600 transition-colors"
        >
          <MapPin className="w-3 h-3" />
          Directions
        </a>
      </div>
    </div>
  );
};

const DoctorCard = ({ doctor }) => {
  return (
    <div className="bg-white rounded-lg p-3 border border-gray-200">
      <div className="flex items-start justify-between mb-2">
        <div>
          <h5 className="font-medium text-sm">{doctor.name}</h5>
          <p className="text-xs text-gray-600">{doctor.specialty}</p>
        </div>
        <div className="flex items-center gap-1 text-xs text-gray-500">
          <Star className="w-3 h-3 fill-yellow-400 text-yellow-400" />
          <span>{doctor.rating}</span>
        </div>
      </div>
      
      <p className="text-xs text-gray-600 mb-1">{doctor.hospital}</p>
      <p className="text-xs text-gray-500 mb-2">Experience: {doctor.experience}</p>
      
      <div className="flex items-center gap-2 text-xs text-gray-600 mb-2">
        <Clock className="w-3 h-3" />
        <span>{doctor.availability}</span>
      </div>
      
      <a
        href={`tel:${doctor.phone}`}
        className="flex items-center gap-1 bg-green-500 text-white px-3 py-1 rounded text-xs hover:bg-green-600 transition-colors w-fit"
      >
        <Phone className="w-3 h-3" />
        Call Doctor
      </a>
    </div>
  );
};

export default ChatMessage;
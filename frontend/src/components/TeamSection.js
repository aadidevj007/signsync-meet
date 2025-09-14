import React from 'react';
import { motion } from 'framer-motion';

const TeamSection = () => {
  const teamMembers = [
    {
      name: "Aadidev",
      role: "AI/ML Engineer",
      image: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&h=150&fit=crop&crop=face",
      description: "Specializes in computer vision and sign language recognition"
    },
    {
      name: "Riya",
      role: "Frontend Developer",
      image: "https://images.unsplash.com/photo-1494790108755-2616b612b786?w=150&h=150&fit=crop&crop=face",
      description: "Expert in React and creating beautiful user experiences"
    },
    {
      name: "Arjun",
      role: "Backend Engineer",
      image: "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150&h=150&fit=crop&crop=face",
      description: "Builds scalable APIs and real-time communication systems"
    },
    {
      name: "Priya",
      role: "UX Designer",
      image: "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=150&h=150&fit=crop&crop=face",
      description: "Designs accessible and inclusive user interfaces"
    }
  ];

  return (
    <section className="px-6 py-20 bg-gradient-to-br from-primary-50 to-purple-50">
      <div className="max-w-7xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          viewport={{ once: true }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl md:text-5xl font-bold mb-6 bg-gradient-to-r from-primary-600 to-purple-600 bg-clip-text text-transparent">
            Created By
          </h2>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Meet the talented team behind SignSync Meet
          </p>
        </motion.div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
          {teamMembers.map((member, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: index * 0.1 }}
              viewport={{ once: true }}
              className="glass-card rounded-2xl p-6 text-center hover:shadow-2xl transition-all duration-300 group"
            >
              <div className="relative mb-4">
                <img
                  src={member.image}
                  alt={member.name}
                  className="w-24 h-24 rounded-full mx-auto object-cover border-4 border-white shadow-lg group-hover:scale-105 transition-transform"
                />
                <div className="absolute -bottom-2 -right-2 w-8 h-8 bg-gradient-to-r from-primary-500 to-primary-600 rounded-full flex items-center justify-center">
                  <span className="text-white text-xs font-bold">✓</span>
                </div>
              </div>
              <h3 className="text-xl font-semibold mb-2 text-gray-800">{member.name}</h3>
              <p className="text-primary-600 font-medium mb-3">{member.role}</p>
              <p className="text-sm text-gray-600 leading-relaxed">{member.description}</p>
            </motion.div>
          ))}
        </div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.4 }}
          viewport={{ once: true }}
          className="text-center mt-12"
        >
          <div className="glass-card rounded-2xl p-8 max-w-2xl mx-auto">
            <h3 className="text-2xl font-bold mb-4 bg-gradient-to-r from-primary-600 to-purple-600 bg-clip-text text-transparent">
              Our Mission
            </h3>
            <p className="text-gray-600 leading-relaxed">
              We believe that communication should be accessible to everyone. SignSync Meet combines 
              cutting-edge AI technology with intuitive design to break down barriers and create 
              inclusive video conferencing experiences for people of all abilities.
            </p>
          </div>
        </motion.div>
      </div>
    </section>
  );
};

export default TeamSection;

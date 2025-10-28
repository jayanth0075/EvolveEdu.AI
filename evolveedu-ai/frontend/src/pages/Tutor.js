import React, { useState } from "react";
import { motion } from 'framer-motion';
import { Brain, Send, MessageSquare, Sparkles } from 'lucide-react';

/**
 * AI Tutor Component
 * Interactive Q&A interface with proper visibility and single state management
 */
export default function Tutor() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);

  const handleAsk = async () => {
    if (!question.trim()) return;
    
    setLoading(true);
    try {
      // Simulate AI processing delay
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Enhanced AI responses with better visibility
      const responses = [
        "Great question! For Data Scientist roles, focus on Python, ML libraries like scikit-learn and pandas, SQL for data manipulation, and build portfolio projects showcasing your skills.",
        "Excellent inquiry! Start with programming fundamentals, then dive into statistics and machine learning. Practice with real datasets and document your learning journey.",
        "Perfect timing to ask! Consider learning cloud platforms (AWS, Azure), version control (Git), and soft skills like communication for presenting insights to stakeholders."
      ];
      
      const randomResponse = responses[Math.floor(Math.random() * responses.length)];
      setAnswer(randomResponse);
    } catch (error) {
      setAnswer("I apologize, but I'm having trouble processing your question right now. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleAsk();
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6 bg-gray-50 min-h-screen">
      {/* Header with better contrast */}
      <div className="mb-8 text-center">
        <div className="flex items-center justify-center gap-3 mb-4">
          <div className="p-3 bg-blue-600 rounded-full">
            <Brain className="h-8 w-8 text-white" />
          </div>
          <h1 className="text-3xl font-bold text-gray-900">AI Career Tutor</h1>
        </div>
        <p className="text-gray-600 text-lg">Ask questions about your career path, skills, and learning journey</p>
      </div>

      {/* Question Input with proper styling */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
        <div className="flex gap-3">
          <div className="flex-1">
            <textarea
              className="w-full p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none text-gray-900"
              rows="3"
              placeholder="Ask your career or study question... (Press Enter to send)"
              value={question}
              onChange={e => setQuestion(e.target.value)}
              onKeyPress={handleKeyPress}
            />
          </div>
          <button 
            className="flex items-center gap-2 px-6 py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-medium rounded-lg transition-colors disabled:cursor-not-allowed"
            onClick={handleAsk}
            disabled={loading || !question.trim()}
          >
            {loading ? (
              <div className="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full"></div>
            ) : (
              <Send className="h-4 w-4" />
            )}
            {loading ? "Thinking..." : "Ask AI"}
          </button>
        </div>
      </div>

      {/* Answer Display with improved visibility */}
      {answer && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-white rounded-lg shadow-sm border border-gray-200 p-6"
        >
          <div className="flex items-start gap-4">
            <div className="p-2 bg-green-100 rounded-full">
              <Sparkles className="h-5 w-5 text-green-600" />
            </div>
            <div className="flex-1">
              <h3 className="text-lg font-semibold text-gray-900 mb-3 flex items-center gap-2">
                <MessageSquare className="h-5 w-5 text-blue-600" />
                AI Tutor Response
              </h3>
              <p className="text-gray-800 leading-relaxed text-base">{answer}</p>
            </div>
          </div>
        </motion.div>
      )}

      {/* Empty state */}
      {!answer && !loading && (
        <div className="text-center py-12">
          <Brain className="h-16 w-16 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">Ready to help!</h3>
          <p className="text-gray-600">Ask me anything about your career development, study plans, or skill building.</p>
        </div>
      )}
    </div>
  );
}

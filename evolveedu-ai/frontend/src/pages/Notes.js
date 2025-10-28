import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { BookOpen, Plus, Search, Filter, FileText } from 'lucide-react';

/**
 * Notes Component
 * Displays user notes and AI-generated summaries with proper visibility
 */
const Notes = () => {
  const [notes, setNotes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    // Single API call to fetch notes
    const fetchNotes = async () => {
      setLoading(true);
      try {
        // Simulated notes data with better visibility
        const mockNotes = [
          {
            id: 1,
            title: 'JavaScript Fundamentals',
            content: 'Key concepts: Variables, Functions, Objects, Arrays',
            category: 'Programming',
            createdAt: '2024-10-20'
          },
          {
            id: 2,
            title: 'React Hooks Overview',
            content: 'useState, useEffect, useContext - modern React patterns',
            category: 'Frontend',
            createdAt: '2024-10-18'
          }
        ];
        setNotes(mockNotes);
      } catch (error) {
        console.error('Failed to fetch notes:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchNotes();
  }, []); // Single dependency array to prevent duplicate calls

  const filteredNotes = notes.filter(note =>
    note.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
    note.content.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="max-w-6xl mx-auto p-6 bg-gray-50 min-h-screen">
      {/* Header with proper contrast */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2 flex items-center gap-3">
          <BookOpen className="h-8 w-8 text-blue-600" />
          Notes & Summaries
        </h1>
        <p className="text-gray-600 text-lg">Your personalized learning notes and AI-generated summaries</p>
      </div>

      {/* Search and Actions */}
      <div className="flex flex-col sm:flex-row gap-4 mb-6">
        <div className="flex-1 relative">
          <Search className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
          <input
            type="text"
            placeholder="Search notes..."
            className="w-full pl-10 pr-4 py-2 bg-white border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-gray-900"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
        <button className="flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors">
          <Plus className="h-4 w-4" />
          Add Note
        </button>
      </div>

      {/* Notes Grid with proper visibility */}
      {loading ? (
        <div className="text-center py-12">
          <div className="text-gray-600">Loading notes...</div>
        </div>
      ) : (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {filteredNotes.map((note) => (
            <motion.div
              key={note.id}
              className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow"
              whileHover={{ y: -4 }}
              transition={{ duration: 0.2 }}
            >
              <div className="flex items-start gap-3 mb-3">
                <FileText className="h-5 w-5 text-blue-600 mt-1" />
                <div className="flex-1">
                  <h3 className="text-lg font-semibold text-gray-900 mb-1">{note.title}</h3>
                  <span className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded-full">
                    {note.category}
                  </span>
                </div>
              </div>
              <p className="text-gray-700 text-sm mb-4 line-clamp-3">{note.content}</p>
              <div className="text-xs text-gray-500">
                Created: {note.createdAt}
              </div>
            </motion.div>
          ))}
        </div>
      )}

      {filteredNotes.length === 0 && !loading && (
        <div className="text-center py-12">
          <FileText className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No notes found</h3>
          <p className="text-gray-600">Start by creating your first note or summary</p>
        </div>
      )}
    </div>
  );
};

export default Notes;
import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import { projectsAPI } from '../services/api';

const Projects = () => {
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    budget: '',
    deadline: ''
  });

  const queryClient = useQueryClient();

  const { data: projects, isLoading, error } = useQuery(
    'projects',
    projectsAPI.getAll
  );

  const createProjectMutation = useMutation(
    projectsAPI.create,
    {
      onSuccess: () => {
        queryClient.invalidateQueries('projects');
        setShowCreateForm(false);
        setFormData({ name: '', description: '', budget: '', deadline: '' });
      }
    }
  );

  const handleSubmit = (e) => {
    e.preventDefault();
    const projectData = {
      ...formData,
      budget: formData.budget ? parseFloat(formData.budget) : null,
      deadline: formData.deadline ? new Date(formData.deadline).toISOString() : null
    };
    createProjectMutation.mutate(projectData);
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  if (isLoading) {
    return (
      <div className="flex justify-center items-center min-h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-red-600 text-center">
        Error loading projects: {error.message}
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-900">Projects</h1>
        <button
          onClick={() => setShowCreateForm(true)}
          className="btn-primary"
        >
          Create Project
        </button>
      </div>

      {showCreateForm && (
        <div className="card">
          <h2 className="text-xl font-semibold mb-4">Create New Project</h2>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="form-label">Project Name</label>
              <input
                type="text"
                name="name"
                value={formData.name}
                onChange={handleChange}
                className="form-input"
                required
              />
            </div>
            
            <div>
              <label className="form-label">Description</label>
              <textarea
                name="description"
                value={formData.description}
                onChange={handleChange}
                className="form-input"
                rows="3"
              ></textarea>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="form-label">Budget</label>
                <input
                  type="number"
                  name="budget"
                  value={formData.budget}
                  onChange={handleChange}
                  className="form-input"
                  placeholder="0.00"
                />
              </div>
              
              <div>
                <label className="form-label">Deadline</label>
                <input
                  type="date"
                  name="deadline"
                  value={formData.deadline}
                  onChange={handleChange}
                  className="form-input"
                />
              </div>
            </div>
            
            <div className="flex space-x-4">
              <button
                type="submit"
                disabled={createProjectMutation.isLoading}
                className="btn-primary"
              >
                {createProjectMutation.isLoading ? 'Creating...' : 'Create Project'}
              </button>
              <button
                type="button"
                onClick={() => setShowCreateForm(false)}
                className="btn-secondary"
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {projects && projects.length > 0 ? (
          projects.map((project) => (
            <div key={project.id} className="card hover:shadow-lg transition-shadow">
              <div className="flex justify-between items-start mb-4">
                <h3 className="text-lg font-semibold text-gray-900">{project.name}</h3>
                <span className={`px-2 py-1 text-xs rounded-full ${{
                  'active': 'bg-green-100 text-green-800',
                  'planning': 'bg-yellow-100 text-yellow-800',
                  'completed': 'bg-blue-100 text-blue-800',
                  'on_hold': 'bg-gray-100 text-gray-800',
                  'cancelled': 'bg-red-100 text-red-800'
                }[project.status] || 'bg-gray-100 text-gray-800'}`}>
                  {project.status.replace('_', ' ')}
                </span>
              </div>
              
              <p className="text-gray-600 mb-4">{project.description || 'No description'}</p>
              
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span className="text-gray-500">Progress</span>
                  <span className="font-medium">{project.progress}%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                    style={{ width: `${project.progress}%` }}
                  ></div>
                </div>
              </div>
              
              {project.budget && (
                <div className="mt-4 flex justify-between text-sm">
                  <span className="text-gray-500">Budget</span>
                  <span className="font-medium">
                    ${project.spent_budget || 0} / ${project.budget}
                  </span>
                </div>
              )}
              
              {project.deadline && (
                <div className="mt-2 flex justify-between text-sm">
                  <span className="text-gray-500">Deadline</span>
                  <span className="font-medium">
                    {new Date(project.deadline).toLocaleDateString()}
                  </span>
                </div>
              )}
              
              <div className="mt-4 flex space-x-2">
                <button className="flex-1 bg-blue-50 text-blue-600 hover:bg-blue-100 px-3 py-2 rounded text-sm font-medium transition-colors">
                  View Details
                </button>
                <button className="flex-1 bg-gray-50 text-gray-600 hover:bg-gray-100 px-3 py-2 rounded text-sm font-medium transition-colors">
                  Edit
                </button>
              </div>
            </div>
          ))
        ) : (
          <div className="col-span-full text-center py-12">
            <svg className="w-16 h-16 mx-auto text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
            </svg>
            <h3 className="text-lg font-medium text-gray-900 mb-2">No projects yet</h3>
            <p className="text-gray-500 mb-4">Get started by creating your first project</p>
            <button
              onClick={() => setShowCreateForm(true)}
              className="btn-primary"
            >
              Create Project
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default Projects;
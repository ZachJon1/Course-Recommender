const express = require('express');
const cors = require('cors');
const axios = require('axios');
const cheerio = require('cheerio');
const { PythonShell } = require('python-shell');
const rateLimit = require('express-rate-limit');
const NodeCache = require('node-cache');
require('dotenv').config();

const app = express();
app.use(cors());
app.use(express.json());

// Create a cache with 2 hour TTL
const courseCache = new NodeCache({ stdTTL: 7200 });

// Add rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // limit each IP to 100 requests per windowMs
  message: "Too many requests from this IP, please try again later"
});

// Apply rate limiting to scraping endpoints
app.use('/api/course', limiter);
app.use('/api/program', limiter);

// Environment variables for LLM
const HOST = process.env.LLM_HOST || "";
const PORT_LLM = process.env.LLM_PORT || "1";
const API_KEY = process.env.LLM_API_KEY || "";

// LLM endpoint
app.post('/api/llm', async (req, res) => {
  const { message, history } = req.body;
  
  try {
    // Run Python script with message
    let options = {
      mode: 'text',
      pythonPath: 'python3',
      scriptPath: '../LLM-Local-Deployment/',
      args: [HOST, PORT_LLM, API_KEY, message, JSON.stringify(history)]
    };
    
    PythonShell.run('llm_wrapper.py', options).then(results => {
      const response = JSON.parse(results[0]);
      res.json(response);
    }).catch(err => {
      console.error('Python script error:', err);
      res.status(500).json({ error: 'Failed to process LLM request', details: err.message });
    });
  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({ error: 'Failed to process LLM request' });
  }
});

// Get all courses for a specific program
app.get('/api/program/:programId/courses', async (req, res) => {
  try {
    const programId = req.params.programId;
    
    // Check cache first
    const cacheKey = `program_${programId}`;
    const cachedData = courseCache.get(cacheKey);
    if (cachedData) {
      return res.json(cachedData);
    }
    
    const catalogUrl = `https://catalog.olemiss.edu/2026/fall/engineering/${programId}/courses`;
    
    console.log(`Scraping courses from: ${catalogUrl}`);
    const response = await axios.get(catalogUrl, {
      headers: {
        'User-Agent': 'CourseRecommendationApp/1.0 (academic-project)'
      },
      timeout: 10000
    });
    
    const html = response.data;
    
    // Parse with cheerio
    const $ = cheerio.load(html);
    const courses = [];
    
    // Extract course listings
    $('.course-listing').each((i, elem) => {
      const courseLink = $(elem).find('.course-code a');
      const courseId = courseLink.text().trim().replace(/\s+/g, '');
      const courseName = $(elem).find('.course-title').text().trim();
      
      // Extract credits
      const courseHours = $(elem).find('.course-hours').text().trim();
      const creditsMatch = courseHours.match(/\((\d+)\)/);
      const credits = creditsMatch ? parseInt(creditsMatch[1]) : 3;
      
      // Extract abbreviated description
      const courseDescription = $(elem).find('.course-description').text().trim();
      
      // Determine level based on course number
      const courseNum = parseInt(courseId.replace(/[A-Z]+/g, ''));
      const level = courseNum < 200 ? 'Introductory' : 
                   courseNum < 400 ? 'Intermediate' : 'Advanced';
      
      courses.push({
        id: courseId,
        name: courseName,
        credits: credits,
        description: courseDescription,
        program: programId,
        department: courseId.match(/^[A-Z]+/)[0],
        level,
        prereqs: [], // Will be populated when specific course details are fetched
        terms: ['Fall', 'Spring'] // Default, actual terms will be fetched with detailed course info
      });
    });
    
    // Cache the results
    courseCache.set(cacheKey, courses);
    
    res.json(courses);
  } catch (error) {
    console.error('Error scraping program courses:', error);
    res.status(500).json({ 
      error: 'Failed to retrieve course catalog',
      details: error.message
    });
  }
});

// Get detailed information for a specific course
app.get('/api/course/:courseId', async (req, res) => {
  try {
    const courseId = req.params.courseId.toUpperCase();
    
    // Check cache first
    const cacheKey = `course_${courseId}`;
    const cachedData = courseCache.get(cacheKey);
    if (cachedData) {
      return res.json(cachedData);
    }
    
    // Extract dept code from course ID
    const deptCode = courseId.match(/^[A-Z]+/)[0].toLowerCase();
    const courseUrl = `https://catalog.olemiss.edu/2026/fall/${deptCode}/courses/${courseId.toLowerCase()}`;
    
    console.log(`Fetching course details from: ${courseUrl}`);
    
    const response = await axios.get(courseUrl, {
      headers: {
        'User-Agent': 'CourseRecommendationApp/1.0 (academic-project)'
      },
      timeout: 10000
    });
    
    const html = response.data;
    const $ = cheerio.load(html);
    
    // Extract course details
    const name = $('.page-title').text().replace(courseId, '').trim();
    const description = $('.course-description').text().trim();
    
    // Extract prerequisites
    const prereqsSection = $('.course-prereqs').text().trim();
    const prereqMatches = prereqsSection.match(/[A-Z]{2,4}\s*\d{3}/g) || [];
    const prereqs = prereqMatches.map(p => p.replace(/\s+/g, ''));
    
    // Extract credits
    const creditText = $('.course-hours').text().trim();
    const creditMatch = creditText.match(/\((\d+)\)/);
    const credits = creditMatch ? parseInt(creditMatch[1]) : 3;
    
    // Extract terms offered (if available)
    const termsText = $('.course-terms').text().trim();
    const terms = termsText
      ? termsText.split(',').map(t => t.trim())
      : ['Fall', 'Spring'];
    
    // Determine level based on course number
    const courseNum = parseInt(courseId.replace(/[A-Z]+/g, ''));
    const level = courseNum < 200 ? 'Introductory' : 
                 courseNum < 400 ? 'Intermediate' : 'Advanced';
    
    // Extract department name
    const department = $('.breadcrumb').text().includes('Computer Science') 
      ? 'Computer Science' 
      : deptCode.toUpperCase();
    
    // Extract professors if available
    const professors = [];
    $('.course-instructor').each((i, elem) => {
      const profName = $(elem).text().trim();
      if (profName) {
        professors.push(profName);
      }
    });
    
    const courseData = {
      id: courseId,
      name,
      description,
      prereqs,
      credits,
      terms,
      professors: professors.length > 0 ? professors : ['TBD'], 
      department,
      level
    };
    
    // Cache the results
    courseCache.set(cacheKey, courseData);
    
    res.json(courseData);
  } catch (error) {
    console.error('Error scraping course details:', error);
    res.status(404).json({ 
      error: 'Course not found or error accessing catalog',
      details: error.message
    });
  }
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
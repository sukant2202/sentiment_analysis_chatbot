# Vercel Deployment Guide

## Prerequisites

1. Install Vercel CLI:
   ```bash
   npm install -g vercel
   ```

2. Make sure you have a Vercel account at [vercel.com](https://vercel.com)

## Deployment Steps

### 1. Login to Vercel
```bash
vercel login
```

### 2. Deploy the Application
```bash
vercel
```

### 3. Follow the Prompts
- Choose to link to existing project or create new
- Set project name (optional)
- Choose your Vercel account/team
- Confirm deployment

### 4. Alternative: Deploy with Project Linking
```bash
vercel --prod
```

## Important Notes

### NLTK Data
The app automatically downloads required NLTK data to `/tmp/nltk_data` on Vercel's serverless environment.

### Environment Variables
If you need to set environment variables:
1. Go to your Vercel dashboard
2. Select your project
3. Go to Settings > Environment Variables
4. Add any required variables

### Static Files
Static files (CSS, JS) are served through Flask's static file handling.

## Troubleshooting

### Common Issues

1. **NLTK Data Not Found**: The app automatically downloads required data on first run
2. **Import Errors**: Ensure all dependencies are in `requirements.txt`
3. **Timeout Issues**: Vercel has a 10-second timeout for serverless functions

### Performance Optimization

- The app uses in-memory conversation storage (resets on each deployment)
- Consider using external databases for production use
- NLTK data is cached in `/tmp` directory

## Monitoring

- Check Vercel dashboard for deployment status
- Monitor function execution logs
- Use the `/health` endpoint to verify app status

## Production Considerations

- Add proper error handling
- Implement rate limiting
- Use external databases for conversation storage
- Add authentication if needed
- Monitor API usage and costs

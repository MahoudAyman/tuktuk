import { createClient } from '@supabase/supabase-js';

// NOTE: In a real production app, use environment variables.
// For this prompt's requirement to work immediately, we use the provided keys.
const SUPABASE_URL = 'https://oljxeosptnsmlcggzogw.supabase.co';
const SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9sanhlb3NwdG5zbWxjZ2d6b2d3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM2NjY3MDksImV4cCI6MjA3OTI0MjcwOX0.niii7MFS8W9GHtjunloo94qxaDPWOq2aeDUu_fZklKk';

export const supabase = createClient(SUPABASE_URL, SUPABASE_KEY);

export const USERS_TABLE = 'users';
export const DRIVERS_TABLE = 'drivers';
export const RIDES_TABLE = 'rides';
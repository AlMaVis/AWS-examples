# Required libraries
require 'aws-sdk-s3'    # AWS SDK for interacting with S3
require 'pry'           # Debugging tool (optional, used for interactive breakpoints)
require 'securerandom'  # For generating unique IDs

# Set the target S3 bucket name from an environment variable
bucket_name = ENV['S3_BUCKET_NAME']

# Define the AWS region to use
region = 'eu-west-3'  # Example: Paris region

# Initialize the S3 client using credentials from environment variables
client = Aws::S3::Client.new(
  region: region,
  access_key_id: ENV['AWS_ACCESS_KEY_ID'],
  secret_access_key: ENV['AWS_SECRET_ACCESS_KEY']
)

# Create the specified S3 bucket in the given region
resp = client.create_bucket(
  bucket: bucket_name,
  create_bucket_configuration: {
    location_constraint: region
  }
)
#binding.pry


# Generate a random number (1–6) of files to create and upload
number_of_files = 1 + rand(6)
puts "Creating #{number_of_files} files in bucket #{bucket_name}"

# Loop to create and upload each file
number_of_files.times.each do |i|
  puts "Creating file #{i + 1}"

  # Create a file with a unique name
  file_name = "file_#{i}.txt"
  output_path = "/tmp/#{file_name}"

  # Write a randomly generated UUID to the file
  File.open(output_path, 'w') do |f|
    f.write SecureRandom.uuid
  end

  # Upload the file to S3
  File.open(output_path, 'rb') do |f|
    client.put_object(
      bucket: bucket_name,
      key: file_name,
      body: f
    )
  end
end

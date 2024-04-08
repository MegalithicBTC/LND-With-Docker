import subprocess
import time
import os

print('starting write zpool status')
while True:
    try:
        # Run zpool status and capture the output
        zpool_status_output = subprocess.check_output(['zpool', 'status'], text=True)
        print(zpool_status_output)
        
        # Create the directory if it doesn't exist
        output_dir = 'pworker/zpool_status'
      
        # Write the output to a text file
        with open(os.path.join(output_dir, 'pool_status.txt'), 'w') as f:
            f.write(zpool_status_output)
        print('wrote zpool status')
        time.sleep(60 * 10) # ten mins
    
    except KeyboardInterrupt:
        # Exit the script when Ctrl+C is pressed
        break
# Smart Attendance System (SAS) - Frontend & Dashboard Specifications

## Document Information
- **Version:** 1.0
- **Date:** December 2, 2025
- **Platform:** Django (Python)
- **AI Backend Integration:** SAS

---

## 1. System Overview

### 1.1 What is SAS?
The Smart Attendance System (SAS) is an AI-powered facial recognition attendance management system that:
- Processes live video feeds from multiple IP/PTZ cameras
- Detects and tracks faces
- Recognizes registered persons
- Records attendance automatically with timestamps and evidence images
- Monitors system health, GPU usage, and camera status in real-time

### 1.2 Current Architecture
```
┌─────────────────────────────────────────────────────────────────┐
│                     SAS AI Backend (Python)                     │
├─────────────────────────────────────────────────────────────────┤
│  • Face Detection                                               │
│  • Face Recognition                                             │
│  • Multi-camera support (4+ cameras per PC)                     │
│  • Real-time tracking                                           │
│  • WebSocket streaming for live feeds                           │
│  • Metrics collection & health monitoring                       │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    MySQL Database (db_sas)                      │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│              Django Frontend (TO BE DEVELOPED)                  │
│  • Dashboard & Analytics                                        │
│  • Person Management                                            │
│  • Camera Management                                            │
│  • Attendance Reports                                           │
│  • System Monitoring                                            │
│  • Real-time Live Feed Viewer                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Database Schema

### 2.1 Existing Tables (Must Support)

#### `person` - Registered Persons
```sql
CREATE TABLE `person` (
    `pid` VARCHAR(50) PRIMARY KEY,           -- Person ID (e.g., "25", "38")
    `person_name` VARCHAR(255) NOT NULL,     -- Full name (e.g., "Dr_Suhail_Yousaf")
    `person_nic` VARCHAR(20),                -- National ID Card number
    `person_father` VARCHAR(255),            -- Father's name
    `person_designation` VARCHAR(100),       -- Job title/designation
    `person_cat` VARCHAR(50),                -- Category (e.g., "1" for employee)
    `person_embedding` TEXT NOT NULL,        -- 128-dim face embedding (space-separated floats)
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

#### `camera_parameters` - Camera Configuration
```sql
CREATE TABLE `camera_parameters` (
    `camera_id` VARCHAR(10) PRIMARY KEY,     -- Camera ID (e.g., "C1", "C2")
    `ip_address` VARCHAR(50) NOT NULL,       -- Camera IP address
    `username` VARCHAR(50) NOT NULL,         -- Camera login username
    `password` VARCHAR(100) NOT NULL,        -- Camera login password
    `cam_type` VARCHAR(20) NOT NULL,         -- "PTZ" or "Fixed"
    
    -- Face Recognition Parameters
    `fr_conf_thresh` FLOAT DEFAULT 0.32,      -- Detection confidence threshold
    `fr_iou_thresh` FLOAT DEFAULT 0.3,       -- IOU threshold for NMS
    `fr_min_avg_thresh` FLOAT DEFAULT 0.5,   -- Min avg threshold for recognition
    `fr_min_frame_count` INT DEFAULT 10,     -- Frames needed for recognition
    `fr_min_frame_count_2` INT DEFAULT 30,   -- Reset interval frames
    `fr_api_counter` INT DEFAULT 1,          -- API counter setting
    
    -- Recognition Settings
    `recognition_t` FLOAT DEFAULT 0.32,       -- Recognition threshold (cosine similarity)
    `dist_method` VARCHAR(20) DEFAULT 'cosine', -- Distance method
    `norm_method` VARCHAR(20) DEFAULT 'fixed',  -- Normalization method
    
    -- API Configuration
    `_sd` VARCHAR(50),                       -- API sd parameter
    `_flag` VARCHAR(50),                     -- API flag parameter
    
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

#### `tbl_camera` - Camera Locations
```sql
CREATE TABLE `tbl_camera` (
    `camera_id` VARCHAR(10) PRIMARY KEY,     -- Camera ID (e.g., "C1")
    `location` VARCHAR(255) NOT NULL,        -- Location name (e.g., "Main Entrance")
    `description` TEXT,
    `attendance_type` ENUM('IN', 'OUT') DEFAULT 'IN',  -- Camera records IN or OUT attendance based on location
    `is_active` BOOLEAN DEFAULT TRUE,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Note:** `attendance_type` determines what type of attendance this camera records:
- `IN` = Camera at entrance (e.g., main gate, lobby entry) - records check-in
- `OUT` = Camera at exit (e.g., exit gate, parking exit) - records check-out

#### `pc_configuration` - Processing PC Registration & Settings
```sql
CREATE TABLE `pc_configuration` (
    `pc_id` VARCHAR(20) PRIMARY KEY,         -- PC identifier (e.g., "PC1", "PC2")
    `pc_name` VARCHAR(100) NOT NULL,         -- Friendly name (e.g., "Main Building Server")
    `ip_address` VARCHAR(50),                -- PC's IP address
    `gpu_count` INT DEFAULT 1,               -- Number of GPUs available
    `gpu_ids` VARCHAR(50) DEFAULT '0',       -- Comma-separated GPU IDs (e.g., "0,1")
    `is_active` BOOLEAN DEFAULT TRUE,        -- Enable/disable this PC
    `last_heartbeat` DATETIME,               -- Last time AI backend reported status
    `status` ENUM('online', 'offline', 'error') DEFAULT 'offline',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

#### `ai_models` - Available AI Models Registry
```sql
CREATE TABLE `ai_models` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `model_type` ENUM('face_detection', 'face_recognition', 'weapon_detection') NOT NULL,
    `model_name` VARCHAR(100) NOT NULL,      -- e.g., "YOLOv5-face-n", "ArcFace-R50"
    `model_version` VARCHAR(20),             -- e.g., "1.0", "2.1"
    `model_path` VARCHAR(500) NOT NULL,      -- Path to model file (e.g., "./weights/fd/yolov5n-face.trt")
    `model_format` ENUM('tensorrt', 'onnx', 'pytorch') DEFAULT 'tensorrt',
    `input_size` VARCHAR(20),                -- e.g., "640x640", "160x160"
    `description` TEXT,
    `is_default` BOOLEAN DEFAULT FALSE,      -- Default model for this type
    `is_active` BOOLEAN DEFAULT TRUE,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE KEY `unique_model` (`model_type`, `model_name`, `model_version`),
    INDEX `idx_model_type` (`model_type`)
);
```

**Example Models:**
| model_type | model_name | model_path | input_size |
|------------|------------|------------|------------|
| face_detection | YOLOv5-face-n | ./weights/fd/yolov5n-face.trt | 640x640 |
| face_detection | YOLOv5-face-s | ./weights/fd/yolov5s-face.trt | 640x640 |
| face_recognition | ArcFace-R50 | ./weights/fr/arcface_r50.trt | 112x112 |
| face_recognition | ArcFace-R18 | ./weights/fr/arcface_r18.trt | 112x112 |
| weapon_detection | YOLOv5-weapon | ./weights/wp/weapon_det.trt | 640x640 |

#### `pc_model_config` - PC-Level Model Assignment
```sql
CREATE TABLE `pc_model_config` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `pc_id` VARCHAR(20) NOT NULL,
    `model_type` ENUM('face_detection', 'face_recognition', 'weapon_detection') NOT NULL,
    `model_id` INT NOT NULL,                 -- FK to ai_models
    `is_active` BOOLEAN DEFAULT TRUE,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    UNIQUE KEY `unique_pc_model_type` (`pc_id`, `model_type`),  -- One model per type per PC
    FOREIGN KEY (`pc_id`) REFERENCES `pc_configuration`(`pc_id`) ON DELETE CASCADE,
    FOREIGN KEY (`model_id`) REFERENCES `ai_models`(`id`)
);
```

**Example:** PC1 uses lightweight models, PC2 uses heavy models:
| pc_id | model_type | model_name |
|-------|------------|------------|
| PC1 | face_detection | YOLOv5-face-n (nano) |
| PC1 | face_recognition | ArcFace-R18 (light) |
| PC2 | face_detection | YOLOv5-face-s (small) |
| PC2 | face_recognition | ArcFace-R50 (heavy) |

#### `cam_pc_conf` - Camera-PC-GPU-Feature Assignment
```sql
CREATE TABLE `cam_pc_conf` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `pc_id` VARCHAR(20) NOT NULL,            -- PC identifier (e.g., "PC1")
    `cam_id` VARCHAR(10) NOT NULL,           -- Camera ID (e.g., "C1")
    `gpu_id` INT DEFAULT 0,                  -- Assigned GPU on this PC (0, 1, 2...)
    
    -- Feature Toggles (per camera on this PC)
    `enable_face_recognition` BOOLEAN DEFAULT TRUE,
    `enable_weapon_detection` BOOLEAN DEFAULT FALSE,
    `enable_tracking` BOOLEAN DEFAULT TRUE,
    `enable_live_stream` BOOLEAN DEFAULT TRUE,
    
    -- Processing Priority
    `priority` INT DEFAULT 5,                -- 1=highest, 10=lowest (for GPU scheduling)
    
    `is_active` BOOLEAN DEFAULT TRUE,        -- Enable/disable this camera on this PC
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    UNIQUE KEY `unique_pc_cam` (`pc_id`, `cam_id`),
    INDEX `idx_pc_gpu` (`pc_id`, `gpu_id`),
    FOREIGN KEY (`pc_id`) REFERENCES `pc_configuration`(`pc_id`) ON DELETE CASCADE,
    FOREIGN KEY (`cam_id`) REFERENCES `tbl_camera`(`camera_id`) ON DELETE CASCADE
);
```

**Example:** Multi-PC, Multi-GPU Setup:
| pc_id | cam_id | gpu_id | FR | WP | Priority |
|-------|--------|--------|-----|-----|----------|
| PC1 | C1 | 0 | ✓ | ✗ | 1 |
| PC1 | C2 | 0 | ✓ | ✗ | 2 |
| PC1 | C3 | 1 | ✓ | ✓ | 1 |
| PC2 | C4 | 0 | ✓ | ✗ | 1 |
| PC2 | C5 | 0 | ✗ | ✓ | 2 |

*PC1 has 2 GPUs: GPU0 handles C1+C2 (FR only), GPU1 handles C3 (FR+WP)*

#### `camera_presets` - PTZ Camera Presets (One-to-Many: each camera can have multiple presets)
```sql
CREATE TABLE `camera_presets` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `camera_id` VARCHAR(10) NOT NULL,
    `preset_token` VARCHAR(10) NOT NULL,     -- PTZ preset token (e.g., '1', '2', '3')
    `preset_name` VARCHAR(100),              -- Human-readable name (e.g., 'Main Entrance', 'Lobby View')
    `preset_time` INT DEFAULT 5,             -- Duration in MINUTES to stay at this preset position
    `preset_delay` INT DEFAULT 0,            -- Delay in seconds before moving to next preset
    `preset_order` INT DEFAULT 0,            -- Order in patrol sequence
    `is_active` BOOLEAN DEFAULT TRUE,        -- Enable/disable individual presets
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX `idx_camera_presets` (`camera_id`),
    INDEX `idx_camera_order` (`camera_id`, `preset_order`),
    UNIQUE KEY `unique_camera_preset` (`camera_id`, `preset_token`),  -- Prevent duplicate preset tokens per camera
    FOREIGN KEY (`camera_id`) REFERENCES `tbl_camera`(`camera_id`) ON DELETE CASCADE
);
```

**Example:** Camera C1 (PTZ) patrol sequence:
| preset_token | preset_name | preset_time (mins) | preset_order |
|--------------|-------------|-------------------|--------------|
| 1 | Main Entrance | 10 | 1 |
| 2 | Lobby View | 5 | 2 |
| 3 | Exit Door | 8 | 3 |

*Camera stays at "Main Entrance" for 10 mins → moves to "Lobby View" for 5 mins → moves to "Exit Door" for 8 mins → repeats*

### 2.2 New Tables (To Be Created)

#### `attendance_records` - Attendance Log
```sql
CREATE TABLE `attendance_records` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `person_id` VARCHAR(50) NOT NULL,
    `person_name` VARCHAR(255) NOT NULL,
    `camera_id` VARCHAR(10) NOT NULL,
    `pc_id` VARCHAR(20) NOT NULL,
    `attendance_type` ENUM('IN', 'OUT') NOT NULL,  -- Derived from camera's attendance_type at time of recording
    `confidence` FLOAT,                      -- Recognition confidence (0-100%)
    `image_path` VARCHAR(500),               -- Path to captured image
    `timestamp` DATETIME NOT NULL,
    `date` DATE NOT NULL,                    -- For quick date-based queries
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX `idx_person_date` (`person_id`, `date`),
    INDEX `idx_date` (`date`),
    INDEX `idx_camera_date` (`camera_id`, `date`),
    INDEX `idx_type_date` (`attendance_type`, `date`),  -- For IN/OUT reports
    FOREIGN KEY (`person_id`) REFERENCES `person`(`pid`),
    FOREIGN KEY (`camera_id`) REFERENCES `tbl_camera`(`camera_id`)
);
```
```
**Note:** `attendance_type` is automatically set based on the camera's `tbl_camera.attendance_type` when the record is created. 
- Person detected on Camera C1 (IN camera) → attendance_type = 'IN'
- Person detected on Camera C5 (OUT camera) → attendance_type = 'OUT'
```

#### `system_metrics` - Performance Metrics
```sql
CREATE TABLE `system_metrics` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `pc_id` VARCHAR(20) NOT NULL,
    `timestamp` DATETIME NOT NULL,
    
    -- CPU Metrics
    `cpu_percent` FLOAT,                     -- CPU usage %
    `cpu_temp_celsius` FLOAT,                -- CPU temperature (if available)
    `cpu_fan_rpm` INT,                       -- CPU fan speed RPM (if available)
    
    -- RAM Metrics
    `memory_percent` FLOAT,                  -- RAM usage %
    `memory_used_mb` FLOAT,                  -- RAM used in MB
    
    -- GPU Metrics (NVIDIA via pynvml)
    `gpu_utilization` FLOAT,                 -- GPU core usage %
    `gpu_memory_percent` FLOAT,              -- GPU VRAM usage %
    `gpu_memory_used_mb` FLOAT,              -- GPU VRAM used in MB
    `gpu_temp_celsius` FLOAT,                -- GPU temperature
    `gpu_fan_percent` FLOAT,                 -- GPU fan speed % (0-100)
    `gpu_power_watts` FLOAT,                 -- GPU power draw in Watts
    
    INDEX `idx_pc_timestamp` (`pc_id`, `timestamp`)
);
```

**Python libraries for metrics collection:**
```python
# GPU metrics (NVIDIA) - add 'pynvml' to requirements.txt
import pynvml
pynvml.nvmlInit()
handle = pynvml.nvmlDeviceGetHandleByIndex(0)
gpu_temp = pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU)
gpu_fan = pynvml.nvmlDeviceGetFanSpeed(handle)  # percentage
gpu_power = pynvml.nvmlDeviceGetPowerUsage(handle) / 1000  # mW to W
gpu_util = pynvml.nvmlDeviceGetUtilizationRates(handle).gpu

# CPU temp (Windows) - add 'wmi' to requirements.txt
import wmi
w = wmi.WMI(namespace="root\\OpenHardwareMonitor")  # Requires OpenHardwareMonitor running
for sensor in w.Sensor():
    if sensor.SensorType == 'Temperature' and 'CPU' in sensor.Name:
        cpu_temp = sensor.Value
```

#### `camera_metrics` - Per-Camera Performance
```sql
CREATE TABLE `camera_metrics` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `camera_id` VARCHAR(10) NOT NULL,
    `pc_id` VARCHAR(20) NOT NULL,
    `timestamp` DATETIME NOT NULL,
    `fps` FLOAT,
    `avg_frame_time_ms` FLOAT,
    `avg_detection_time_ms` FLOAT,
    `avg_recognition_time_ms` FLOAT,
    `frames_processed` BIGINT,
    `frames_dropped` BIGINT,
    `faces_detected` INT,
    `faces_recognized` INT,
    `status` ENUM('running', 'paused', 'error', 'stopped'),
    
    INDEX `idx_camera_timestamp` (`camera_id`, `timestamp`)
);
```

#### `system_alerts` - Alerts & Notifications
```sql
CREATE TABLE `system_alerts` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `pc_id` VARCHAR(20),
    `camera_id` VARCHAR(10),
    `timestamp` DATETIME NOT NULL,
    `level` ENUM('info', 'warning', 'critical') NOT NULL,
    `category` ENUM('fps', 'memory', 'gpu', 'api', 'camera', 'system') NOT NULL,
    `message` TEXT NOT NULL,
    `value` FLOAT,
    `threshold` FLOAT,
    `is_acknowledged` BOOLEAN DEFAULT FALSE,
    `acknowledged_by` VARCHAR(100),
    `acknowledged_at` DATETIME,
    
    INDEX `idx_timestamp` (`timestamp`),
    INDEX `idx_level` (`level`),
    INDEX `idx_unacknowledged` (`is_acknowledged`, `timestamp`)
);
```

#### `users` - System Users (Django Auth Extended)
```sql
-- Use Django's built-in User model, extend with:
CREATE TABLE `user_profile` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `user_id` INT NOT NULL UNIQUE,           -- Django User FK
    `role` ENUM('admin', 'manager', 'viewer') DEFAULT 'viewer',
    `department` VARCHAR(100),
    `can_manage_persons` BOOLEAN DEFAULT FALSE,
    `can_manage_cameras` BOOLEAN DEFAULT FALSE,
    `can_view_reports` BOOLEAN DEFAULT TRUE,
    `can_export_data` BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (`user_id`) REFERENCES `auth_user`(`id`)
);
```

#### `attendance_schedules` - Working Hours Configuration
```sql
CREATE TABLE `attendance_schedules` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(100) NOT NULL,
    `in_time_start` TIME NOT NULL,           -- e.g., "07:30:00"
    `in_time_end` TIME NOT NULL,             -- e.g., "19:00:00"
    `out_time_start` TIME,                   -- e.g., "20:00:00"
    `out_time_end` TIME,                     -- e.g., "21:00:00"
    `is_active` BOOLEAN DEFAULT TRUE,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 3. Django Application Structure

### 3.1 Recommended Project Structure
```
sas_dashboard/
├── manage.py
├── requirements.txt
├── sas_dashboard/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py                    # For WebSocket support
│
├── apps/
│   ├── core/                      # Core utilities, base models
│   │   ├── models.py
│   │   ├── views.py
│   │   └── utils.py
│   │
│   ├── accounts/                  # User management
│   │   ├── models.py              # UserProfile
│   │   ├── views.py
│   │   └── forms.py
│   │
│   ├── persons/                   # Person/Employee management
│   │   ├── models.py              # Person model
│   │   ├── views.py
│   │   ├── forms.py
│   │   └── api/                   # DRF API views
│   │
│   ├── cameras/                   # Camera management
│   │   ├── models.py              # Camera, CameraParameters, CamPcConf
│   │   ├── views.py
│   │   └── api/
│   │
│   ├── attendance/                # Attendance management
│   │   ├── models.py              # AttendanceRecord
│   │   ├── views.py
│   │   └── api/
│   │
│   ├── monitoring/                # System monitoring
│   │   ├── models.py              # SystemMetrics, CameraMetrics, SystemAlerts
│   │   ├── views.py
│   │   ├── consumers.py           # WebSocket consumers
│   │   └── api/
│   │
│   └── reports/                   # Reports & Analytics
│       ├── views.py
│       └── exports.py
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── templates/
│   ├── base.html
│   ├── dashboard/
│   ├── persons/
│   ├── cameras/
│   ├── attendance/
│   ├── monitoring/
│   └── reports/
│
└── media/                         # Uploaded files
    ├── person_photos/
    └── attendance_images/
```

### 3.2 Key Dependencies
```txt
# requirements.txt
Django>=4.2
djangorestframework>=3.14
django-cors-headers>=4.0
channels>=4.0                      # WebSocket support
channels-redis>=4.1                # Redis channel layer
daphne>=4.0                        # ASGI server
celery>=5.3                        # Background tasks
redis>=4.5                         # Caching & message broker
mysqlclient>=2.1                   # MySQL connector
Pillow>=10.0                       # Image processing
numpy>=1.24                        # For embedding operations
django-filter>=23.0                # API filtering
django-import-export>=3.2          # Excel/CSV import/export
openpyxl>=3.1                      # Excel support
reportlab>=4.0                     # PDF generation
python-dateutil>=2.8               # Date utilities
whitenoise>=6.5                    # Static files
gunicorn>=21.0                     # Production server
```

---

## 4. Feature Specifications

### 4.1 Dashboard (Home)

#### 4.1.1 Overview Widgets
| Widget | Description | Data Source |
|--------|-------------|-------------|
| **Today's Attendance Summary** | Present/Absent/Late counts | `attendance_records` |
| **Active Cameras** | Status of all cameras (running/error/stopped) | `camera_metrics` |
| **System Health** | CPU, Memory, GPU usage gauges | `system_metrics` |
| **Recent Alerts** | Last 10 system alerts | `system_alerts` |
| **Real-time Recognition Feed** | Live attendance events | WebSocket |
| **Weekly Attendance Trend** | Line chart of attendance | `attendance_records` |

#### 4.1.2 Quick Actions
- View all attendance today
- Add new person
- Check camera status
- Export today's report
- View system alerts

### 4.2 Person Management

#### 4.2.1 Person List View
- Paginated table with search/filter
- Columns: Photo, ID, Name, Designation, Category, Actions
- Filters: Category, Designation, Created Date
- Bulk actions: Export, Activate/Deactivate

#### 4.2.2 Person Detail View
- Profile photo (extracted from `person_photos/`)
- Personal information (name, NIC, father, designation)
- Attendance history (last 30 days)
- Monthly attendance calendar view
- Face embedding status indicator

#### 4.2.3 Add/Edit Person
**Form Fields:**
- Person ID (auto-generated or manual)
- Full Name (required)
- NIC Number
- Father's Name
- Designation (dropdown)
- Category (dropdown: Employee, Visitor, Contractor, etc.)
- Profile Photo (upload)

**Face Enrollment Process:**

1. **Photo Upload**
   - Upload 3-5 photos of the person (minimum 3 required)
   - Recommended: different angles (front, slight left, slight right)
   - Minimum resolution: 200x200 pixels per face
   - Supported formats: JPG, PNG
   - Max file size: 5MB per image

2. **Photo Validation (Frontend)**
   - Check file format and size
   - Preview thumbnails before submission
   - Allow remove/replace individual photos

3. **Face Detection & Quality Check (Backend API)**
   - Detect face in each uploaded image
   - Reject images with: no face, multiple faces, blurry face, face too small
   - Return quality score per image (0-100%):
     - Face size score (larger = better)
     - Sharpness score (less blur = better)
     - Angle score (frontal = better)

4. **Embedding Generation**
   - Extract 128-dimensional face embedding from each valid photo
   - This creates a "cluster" of embeddings for the person in 128-D space
   - Normalize each embedding vector (L2 normalization)

5. **Cluster Overlap Check (Duplicate/Conflict Detection)**
   - Compare new embeddings against ALL existing person embeddings in database
   - Calculate cosine similarity between new cluster and existing clusters
   - **Check for conflicts:**
     - If similarity > 0.75 with existing person → **WARNING: Possible duplicate**
       - Show: "This person may already be enrolled as [Name] (XX% match)"
       - Allow admin to: Merge, Override, or Cancel
     - If similarity > 0.60 with existing person → **CAUTION: Close match**
       - Show: "Similar to existing person [Name] (XX% match)"
       - Warn that recognition confusion may occur
     - If similarity < 0.40 with all existing → **OK: Unique identity**
   - Display visual similarity report showing top 3 closest matches
   
6. **Final Embedding Storage**
   - Average all valid embeddings into single 128-D vector (centroid of cluster)
   - OR store multiple embeddings per person for better coverage (optional)
   - Save as space-separated floats in `person.person_embedding`

7. **UI Feedback**
   - Show per-image status: ✓ Accepted / ✗ Rejected (with reason)
   - Display overall enrollment quality score
   - Show face crop preview for each accepted image
   - Warning if < 3 images pass quality check
   - Show similarity check results (duplicate/conflict warnings)

8. **Store in Database**
   - Save embedding as space-separated floats in `person.person_embedding`
   - Save best photo as profile picture in `media/person_photos/{pid}.jpg`
   - Update person record with enrollment timestamp
   - Log enrollment action in audit trail

#### 4.2.4 API Endpoints
```
GET    /api/persons/                    # List all persons
POST   /api/persons/                    # Create new person
GET    /api/persons/{pid}/              # Get person details
PUT    /api/persons/{pid}/              # Update person
DELETE /api/persons/{pid}/              # Delete person
POST   /api/persons/{pid}/enroll/       # Enroll face
GET    /api/persons/{pid}/attendance/   # Person's attendance
```

### 4.3 Camera Management

#### 4.3.1 Camera Grid View
- Card-based layout showing all cameras
- Live thumbnail preview (via WebSocket)
- Status indicator (green=running, yellow=connecting, red=error)
- Quick stats: FPS, faces detected today

#### 4.3.2 Camera Detail View
- Live video feed (full size)
- Real-time metrics: FPS, detection time, recognition time
- Camera parameters panel
- PTZ controls (if applicable)
- Recent recognitions from this camera

#### 4.3.3 Camera Configuration Form
**Fields:**
- Camera ID
- Location Name
- IP Address
- Username/Password
- Camera Type (PTZ/Fixed)
- Assigned PC
- Enable FR (checkbox)
- Enable WP (checkbox) - Future weapon detection
- FR Confidence Threshold (slider 0-1)
- FR IOU Threshold (slider 0-1)
- Recognition Threshold (slider 0-1)
- Min Frame Count (number)

#### 4.3.4 API Endpoints
```
GET    /api/cameras/                    # List all cameras
POST   /api/cameras/                    # Add new camera
GET    /api/cameras/{camera_id}/        # Get camera details
PUT    /api/cameras/{camera_id}/        # Update camera
DELETE /api/cameras/{camera_id}/        # Delete camera
GET    /api/cameras/{camera_id}/metrics/ # Camera metrics
GET    /api/cameras/{camera_id}/stream/  # WebSocket stream URL
POST   /api/cameras/{camera_id}/ptz/    # PTZ control commands
```

### 4.4 Attendance Management

#### 4.4.1 Attendance List View
- Date picker (default: today)
- Table columns: Time, Photo, Person ID, Name, Camera, Type (IN/OUT), Confidence
- Filters: Date range, Person, Camera, Type
- Search by name
- Export to Excel/PDF

#### 4.4.2 Attendance Detail Modal
- Full captured image
- Person info
- Timestamp
- Confidence score
- Camera location
- Option to mark as manual entry/correction

#### 4.4.3 Daily Attendance Report
- Summary: Total present, absent, late, early leave
- Detailed table with IN/OUT times
- Highlight anomalies (multiple IN without OUT)

#### 4.4.4 Manual Attendance Entry
- Select person (autocomplete)
- Select date/time
- Select type (IN/OUT)
- Add reason/note

#### 4.4.5 API Endpoints
```
GET    /api/attendance/                 # List attendance records
POST   /api/attendance/                 # Manual entry
GET    /api/attendance/{id}/            # Get record details
PUT    /api/attendance/{id}/            # Update/correct record
DELETE /api/attendance/{id}/            # Delete record
GET    /api/attendance/summary/         # Daily/weekly/monthly summary
GET    /api/attendance/export/          # Export data (Excel/PDF)
```

### 4.5 System Monitoring

#### 4.5.1 Real-time Dashboard
**System Metrics Panel:**
- CPU Usage (gauge + history chart)
- RAM Usage (gauge + history chart)
- GPU Memory (gauge + history chart)
- GPU Utilization (gauge)

**Per-Camera Metrics:**
- FPS (target: 30-50)
- Frame Processing Time
- Detection Time
- Recognition Time
- Faces Detected (today)
- Recognition Success Rate

#### 4.5.2 Alerts Panel
- Real-time alert stream
- Filter by level (info/warning/critical)
- Filter by category (fps/memory/gpu/api/camera)
- Acknowledge button
- Alert history with pagination

#### 4.5.3 Health Check Endpoint Integration
The AI backend exposes health endpoints:
- `GET http://localhost:8081/health` - System health status
- `GET http://localhost:8081/metrics` - Current metrics
- `GET http://localhost:8081/alerts` - Recent alerts

#### 4.5.4 API Endpoints
```
GET    /api/monitoring/health/          # Overall system health
GET    /api/monitoring/metrics/         # Current system metrics
GET    /api/monitoring/metrics/history/ # Historical metrics
GET    /api/monitoring/alerts/          # List alerts
PUT    /api/monitoring/alerts/{id}/acknowledge/ # Acknowledge alert
GET    /api/monitoring/cameras/status/  # All camera statuses
```

### 4.6 Reports & Analytics

#### 4.6.1 Attendance Reports
| Report Type | Description |
|-------------|-------------|
| Daily Report | All attendance for a specific date |
| Weekly Summary | Week-over-week attendance trends |
| Monthly Report | Full month attendance with statistics |
| Person Report | Individual's attendance over a period |
| Department Report | Grouped by department/category |
| Late Arrivals | People who came after threshold time |
| Absentee Report | People not marked on specific dates |

#### 4.6.2 System Reports
| Report Type | Description |
|-------------|-------------|
| Camera Uptime | Camera availability over time |
| Recognition Accuracy | True positives vs false recognitions |
| System Performance | CPU/GPU/Memory trends |
| Alert Summary | Alerts grouped by type and camera |

#### 4.6.3 Export Formats
- Excel (.xlsx) - Detailed data with multiple sheets
- PDF - Formatted printable reports
- CSV - Raw data export

#### 4.6.4 API Endpoints
```
GET    /api/reports/attendance/daily/
GET    /api/reports/attendance/weekly/
GET    /api/reports/attendance/monthly/
GET    /api/reports/attendance/person/{pid}/
GET    /api/reports/system/uptime/
GET    /api/reports/system/performance/
POST   /api/reports/export/             # Generate export file
```

### 4.7 System Configuration (Admin Only)

#### 4.7.1 PC Management
**PC List View:**
- Table of all registered processing PCs
- Columns: PC ID, Name, IP, GPUs, Status (online/offline), Last Heartbeat, Actions
- Status indicator with real-time heartbeat monitoring

**PC Configuration Form:**
- PC ID (unique identifier)
- PC Name (friendly name)
- IP Address
- Number of GPUs
- GPU IDs (comma-separated, e.g., "0,1")
- Active/Inactive toggle

**PC Detail View:**
- Current status and uptime
- Assigned cameras list with GPU allocation
- Active models for this PC
- Real-time metrics from this PC
- Restart/Stop controls (if supported)

#### 4.7.2 AI Model Management
**Model Registry View:**
- Table of all available AI models
- Columns: Type (FD/FR/WP), Name, Version, Format, Input Size, Default, Active
- Filter by model type

**Add/Edit Model Form:**
- Model Type (dropdown: Face Detection, Face Recognition, Weapon Detection)
- Model Name
- Model Version
- Model Path (file path on processing PC)
- Model Format (TensorRT, ONNX, PyTorch)
- Input Size (e.g., "640x640")
- Description
- Set as Default (checkbox)
- Active (checkbox)

**Model Upload (Optional):**
- Upload model file to server
- Auto-distribute to selected PCs

#### 4.7.3 PC Model Assignment
**Assignment Matrix View:**
- Grid showing: PCs (rows) × Model Types (columns)
- Each cell shows currently assigned model
- Click to change model assignment

**Assignment Form:**
- Select PC
- Select Model Type
- Select Model (from available models of that type)
- Apply button

**Bulk Assignment:**
- Select multiple PCs
- Assign same model to all selected

#### 4.7.4 Camera-PC-GPU Assignment
**Assignment Dashboard:**
- Visual grid: Cameras vs PCs
- Drag-and-drop cameras to PCs
- Color-coded by GPU assignment

**Assignment Configuration:**
| Field | Description |
|-------|-------------|
| Camera | Select camera |
| PC | Select processing PC |
| GPU ID | Select GPU on that PC (0, 1, 2...) |
| Enable FR | Face Recognition toggle |
| Enable WP | Weapon Detection toggle |
| Enable Tracking | Object tracking toggle |
| Enable Live Stream | WebSocket streaming toggle |
| Priority | Processing priority (1-10) |

**Validation Rules:**
- Warn if GPU is overloaded (too many cameras)
- Warn if camera already assigned to another PC
- Show estimated GPU memory usage per assignment

#### 4.7.5 Configuration Sync
After changing PC/model/camera assignments:
1. Show "Configuration Changed" indicator
2. "Apply Changes" button to sync to AI backend
3. Options:
   - Apply immediately (may cause brief interruption)
   - Schedule for off-hours
   - Apply on next AI backend restart
4. Show sync status per PC (synced/pending/failed)

#### 4.7.6 API Endpoints
```
# PC Management
GET    /api/config/pcs/                      # List all PCs
POST   /api/config/pcs/                      # Register new PC
GET    /api/config/pcs/{pc_id}/              # Get PC details
PUT    /api/config/pcs/{pc_id}/              # Update PC
DELETE /api/config/pcs/{pc_id}/              # Remove PC
GET    /api/config/pcs/{pc_id}/status/       # Get PC status/heartbeat

# Model Management
GET    /api/config/models/                   # List all models
POST   /api/config/models/                   # Add new model
GET    /api/config/models/{id}/              # Get model details
PUT    /api/config/models/{id}/              # Update model
DELETE /api/config/models/{id}/              # Remove model

# PC-Model Assignment
GET    /api/config/pcs/{pc_id}/models/       # Get models assigned to PC
PUT    /api/config/pcs/{pc_id}/models/       # Update model assignments

# Camera-PC Assignment
GET    /api/config/assignments/              # List all camera-PC assignments
POST   /api/config/assignments/              # Create assignment
PUT    /api/config/assignments/{id}/         # Update assignment
DELETE /api/config/assignments/{id}/         # Remove assignment
GET    /api/config/pcs/{pc_id}/cameras/      # Get cameras assigned to PC

# Sync
POST   /api/config/sync/                     # Trigger config sync to AI backends
GET    /api/config/sync/status/              # Get sync status per PC
```

---

## 5. Real-time Features (WebSocket)

### 5.1 WebSocket Channels

#### 5.1.1 Live Camera Feed
```python
# Consumer: LiveFeedConsumer
# URL: ws://server/ws/camera/{camera_id}/feed/
# Message format:
{
    "type": "frame",
    "camera_id": "C1",
    "timestamp": "2025-12-02T10:30:00",
    "image": "base64_encoded_jpeg",
    "faces_detected": 3,
    "recognitions": [
        {"person_id": "25", "name": "Dr_Suhail", "confidence": 85.5}
    ]
}
```

#### 5.1.2 Attendance Events
```python
# Consumer: AttendanceConsumer
# URL: ws://server/ws/attendance/
# Message format:
{
    "type": "attendance_event",
    "person_id": "25",
    "person_name": "Dr_Suhail_Yousaf",
    "camera_id": "C1",
    "camera_location": "Main Entrance",
    "attendance_type": "IN",
    "confidence": 85.5,
    "timestamp": "2025-12-02T10:30:00",
    "image_url": "/media/attendance/2025-12-02/capture_001.jpg"
}
```

#### 5.1.3 System Alerts
```python
# Consumer: AlertsConsumer
# URL: ws://server/ws/alerts/
# Message format:
{
    "type": "alert",
    "level": "warning",
    "category": "fps",
    "camera_id": "C1",
    "message": "Camera C1: Low FPS (4.5)",
    "value": 4.5,
    "threshold": 5.0,
    "timestamp": "2025-12-02T10:30:00"
}
```

#### 5.1.4 Metrics Updates
```python
# Consumer: MetricsConsumer  
# URL: ws://server/ws/metrics/
# Message format:
{
    "type": "metrics_update",
    "timestamp": "2025-12-02T10:30:00",
    "system": {
        "cpu_percent": 45.2,
        "memory_percent": 62.5,
        "gpu_memory_percent": 78.3
    },
    "cameras": {
        "C1": {"fps": 47.5, "status": "running", "faces_detected": 3},
        "C2": {"fps": 45.2, "status": "running", "faces_detected": 1}
    }
}
```

### 5.2 Django Channels Configuration
```python
# sas_dashboard/asgi.py
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from apps.monitoring import routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sas_dashboard.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns
        )
    ),
})
```

---

## 6. Integration with AI Backend

### 6.1 AI Backend Communication

The Django application needs to communicate with the SAS AI backend for:

#### 6.1.1 Face Enrollment
When adding a new person, the frontend must:
1. Collect 3-5 photos of the person
2. Send to AI backend for embedding generation
3. Store the 128-dimensional embedding in the database

**Proposed Endpoint (to be added to AI backend):**
```
POST http://localhost:8082/api/enroll/
Content-Type: multipart/form-data

{
    "person_id": "50",
    "person_name": "John_Doe",
    "images": [image1.jpg, image2.jpg, image3.jpg]
}

Response:
{
    "success": true,
    "person_id": "50",
    "embedding": "0.123 -0.456 0.789 ...",  // 128 floats
    "quality_score": 0.85
}
```

#### 6.1.2 Attendance Data Collection
The AI backend sends attendance data via PHP API:
```
POST http://localhost/proj/NCAI/SAS/API/datacollection_sas.php

Parameters:
- sd: Source device identifier
- flag: Operation flag
- mid: Camera ID (e.g., "C1")
- pid: Person ID (e.g., "25")
- picture: Image path
- datetime: Timestamp (YYYY-MM-DD HH:MM:SS)
```

**Recommendation:** Create a Django REST endpoint that the AI backend can call directly:
```
POST /api/attendance/record/
{
    "person_id": "25",
    "camera_id": "C1",
    "pc_id": "PC1",
    "attendance_type": "IN",
    "confidence": 85.5,
    "image_base64": "...",
    "timestamp": "2025-12-02 10:30:00"
}
```

#### 6.1.3 Metrics Collection
Poll the AI backend's health endpoints or set up a push mechanism:

**Option A: Polling (simpler)**
- Django Celery task runs every 30 seconds
- Calls `http://localhost:8081/metrics`
- Stores in `system_metrics` and `camera_metrics` tables

**Option B: Push (better)**
- Modify AI backend to POST metrics to Django
- Django receives and stores metrics
- Broadcasts via WebSocket to connected clients

### 6.2 Shared Database Access

Both Django and the AI backend share the same MySQL database (`db_sas`). Key considerations:

1. **Read operations** - Django reads person/camera data for display
2. **Write operations** - Both can write attendance records
3. **Concurrent access** - Use database transactions appropriately
4. **Embedding format** - Space-separated float string (128 values)

Example embedding handling in Django:
```python
# models.py
class Person(models.Model):
    pid = models.CharField(max_length=50, primary_key=True)
    person_name = models.CharField(max_length=255)
    person_embedding = models.TextField()  # Space-separated floats
    
    def get_embedding_array(self):
        """Convert stored embedding to numpy array"""
        import numpy as np
        return np.array([float(x) for x in self.person_embedding.split()])
    
    def set_embedding_array(self, embedding):
        """Store numpy array as space-separated string"""
        self.person_embedding = ' '.join([str(x) for x in embedding])
```

---

## 7. User Interface Guidelines

### 7.1 Design System

#### Color Palette
| Usage | Color | Hex |
|-------|-------|-----|
| Primary | Deep Blue | #1A365D |
| Secondary | Teal | #319795 |
| Success | Green | #38A169 |
| Warning | Yellow | #D69E2E |
| Error | Red | #E53E3E |
| Background | Light Gray | #F7FAFC |
| Card Background | White | #FFFFFF |
| Text Primary | Dark Gray | #2D3748 |
| Text Secondary | Medium Gray | #718096 |

#### Typography
- **Headings:** Inter or Poppins (bold)
- **Body:** Inter or Roboto (regular)
- **Monospace:** JetBrains Mono (for IDs, timestamps)

### 7.2 Component Library
Recommended: **Tailwind CSS** + **DaisyUI** or **ShadCN**

Key Components:
- Dashboard cards with hover effects
- Data tables with sorting/filtering
- Real-time status indicators (pulsing dots)
- Progress bars for system metrics
- Modal dialogs for quick actions
- Toast notifications for alerts
- Calendar heat maps for attendance

### 7.3 Responsive Design
- Desktop-first approach
- Minimum supported width: 1024px
- Mobile view for attendance checking (read-only)

### 7.4 Accessibility
- ARIA labels on all interactive elements
- Keyboard navigation support
- High contrast mode option
- Screen reader compatible tables

---

## 8. Security Requirements

### 8.1 Authentication
- Django session-based authentication
- Password complexity requirements (min 8 chars, mixed case, numbers)
- Account lockout after 5 failed attempts
- Optional: 2FA for admin accounts

### 8.2 Authorization
| Role | Permissions |
|------|-------------|
| Admin | Full access to all features |
| Manager | View all, manage persons, view reports, export data |
| Viewer | View dashboard, view attendance (read-only) |

### 8.3 Data Protection
- HTTPS only in production
- Camera passwords encrypted in database
- Attendance images stored with unique hashed filenames
- Audit log for sensitive operations (person add/delete)

### 8.4 API Security
- Token-based authentication for API endpoints
- Rate limiting (100 requests/minute per user)
- Input validation and sanitization
- CORS configuration for allowed origins

---

## 9. Deployment Requirements

### 9.1 Server Requirements
- **OS:** Ubuntu 22.04 LTS or Windows Server 2019+
- **Python:** 3.10+
- **Database:** MySQL 8.0+
- **Memory:** 4GB minimum, 8GB recommended
- **Storage:** 100GB+ for attendance images

### 9.2 Service Stack
```
┌─────────────────────────────────────────┐
│              Nginx (Reverse Proxy)       │
│        Port 80/443 (HTTP/HTTPS)         │
└─────────────────────────────────────────┘
                    │
        ┌───────────┴───────────┐
        │                       │
        ▼                       ▼
┌───────────────┐       ┌───────────────┐
│    Daphne     │       │   Gunicorn    │
│   (WebSocket) │       │    (HTTP)     │
│   Port 8001   │       │   Port 8000   │
└───────────────┘       └───────────────┘
        │                       │
        └───────────┬───────────┘
                    │
                    ▼
        ┌─────────────────────┐
        │      Django App     │
        └─────────────────────┘
                    │
        ┌───────────┴───────────┐
        │                       │
        ▼                       ▼
┌───────────────┐       ┌───────────────┐
│     MySQL     │       │     Redis     │
│   Port 3306   │       │   Port 6379   │
└───────────────┘       └───────────────┘
```

### 9.3 Environment Variables
```bash
# .env file
DEBUG=False
SECRET_KEY=your-secret-key-here
DATABASE_URL=mysql://user:password@localhost:3306/db_sas
REDIS_URL=redis://localhost:6379/0
ALLOWED_HOSTS=sas.yourdomain.com
AI_BACKEND_URL=http://localhost:8081
MEDIA_ROOT=/var/www/sas/media
STATIC_ROOT=/var/www/sas/static
```

---

## 10. API Documentation

### 10.1 API Standards
- RESTful design principles
- JSON request/response format
- Pagination: `?page=1&page_size=20`
- Filtering: `?date=2025-12-02&camera=C1`
- Sorting: `?ordering=-timestamp`

### 10.2 Response Format
```json
// Success
{
    "status": "success",
    "data": { ... },
    "message": "Operation completed successfully"
}

// Error
{
    "status": "error",
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "errors": {
        "field_name": ["Error message"]
    }
}

// Paginated List
{
    "status": "success",
    "data": {
        "count": 150,
        "next": "/api/attendance/?page=2",
        "previous": null,
        "results": [ ... ]
    }
}
```

### 10.3 Authentication Header
```
Authorization: Token <your-api-token>
```

---

## 11. Testing Requirements

### 11.1 Test Coverage
- Unit tests for all models
- Integration tests for API endpoints
- WebSocket connection tests
- UI component tests (optional: Selenium)

### 11.2 Test Data
Provide fixtures for:
- 50+ sample persons with embeddings
- 8 cameras across 2 PCs
- 1000+ attendance records (30 days)
- Sample metrics and alerts

---

## 12. Timeline Estimate

| Phase | Description |
|-------|-------------|
| Phase 1 | Project setup, models, basic CRUD |
| Phase 2 | Dashboard, person management |
| Phase 3 | Camera management, live feeds |
| Phase 4 | Attendance management, reports |
| Phase 5 | System monitoring, WebSocket |
| Phase 6 | Testing, bug fixes, optimization |

---

## 13. Appendix

### 13.1 Existing File Locations
- **AI Backend:** `C:/xampp/htdocs/proj/NCAI/SAS/SAS_AI/SAS_v14/`
- **Config File:** `config.yaml`
- **Metrics Logs:** `logs/metrics/`
- **System Logs:** `logs/sas_*.log`
- **Attendance Images:** Configurable via `main_dir` in config

### 13.2 Sample Metrics JSON
```json
{
  "export_time": "2025-12-01T18:59:51",
  "summary": {
    "timestamp": "2025-12-01T18:59:51",
    "uptime_seconds": 16508.70,
    "cameras_active": 1,
    "cameras_total": 1,
    "average_fps": 46.83,
    "total_frames_processed": 358302,
    "total_frames_dropped": 0,
    "drop_rate_percent": 0.0,
    "total_faces_detected": 28363,
    "total_faces_recognized": 0,
    "recognition_rate_percent": 0.0,
    "system": {
      "cpu_percent": 8.7,
      "memory_percent": 24.1,
      "memory_used_mb": 31490.3,
      "gpu_memory_percent": 0.1,
      "gpu_memory_used_mb": 13.0
    },
    "recent_alerts": 0
  },
  "cameras": {
    "4": {
      "cam_id": 4,
      "fps": 46.83,
      "avg_frame_time_ms": 21.35,
      "avg_detection_time_ms": 10.66,
      "avg_recognition_time_ms": 0.02,
      "total_faces_detected": 28363,
      "total_faces_recognized": 0,
      "frames_processed": 358302,
      "frames_dropped": 0,
      "status": "running"
    }
  },
  "alerts": []
}
```

### 13.3 Contact
For questions about the AI backend integration, contact the AI team.

---

**Document End**


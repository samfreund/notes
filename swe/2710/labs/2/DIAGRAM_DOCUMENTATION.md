# WearOS Health Monitoring System - Sequence Diagrams Documentation

## Overview
This document provides detailed information about the two sequence diagrams created for the WearOS Health Monitoring System project.

---

## Diagram 1: Trade Worker BPM Display

### Purpose
Models the interaction flow when a trade worker glances at their smartwatch to view their current heart rate and daily average BPM.

### Preconditions
1. Trade worker has WearOS watch powered on and worn correctly
2. HeartRate monitoring app is running and has been active since start of workday
3. HealthServices permissions granted (BODY_SENSORS)
4. At least 5 BPM readings collected during current workday
5. Current time is during work hours (e.g., 10:34 AM)

### Participants

#### View Components (Stereotype: <<View>>)
- **workStatusDisplay:WorkStatusDisplay**
  - Main watch face display
  - Responsible for UI updates and user interaction
  - Methods:
    - `+onResume() : void`
    - `+refreshHeartRateData() : void`
    - `-updateBpmDisplay(model: BpmDisplayModel) : void`

#### Controller Components (Stereotype: <<Controller>>)
- **heartRateController:HeartRateController**
  - Orchestrates data flow between model and view
  - Business logic for display model creation
  - Methods:
    - `+refreshHeartRateData() : void`
    - `+getCurrentHeartRate() : HeartRateReading`
    - `-createDisplayModel(current: HeartRateReading, average: double) : BpmDisplayModel`

- **statsCalculator:StatisticsCalculator**
  - **KEY RESPONSIBILITY: Calculates daily average BPM**
  - Filters outliers and computes statistics
  - Methods:
    - `+calculateDailyAverage(workerId: String) : double`
    - `-computeAverage(readings: List<HeartRateReading>) : double`

#### Model Components (Stereotype: <<Model>>)
- **healthDataRepo:HealthDataRepository**
  - Data access layer for health metrics
  - Interfaces with WearOS HealthServices
  - Methods:
    - `+getCurrentHeartRate() : HeartRateReading`
    - `-createHeartRateReading(dataPoint: DataPoint) : HeartRateReading`

- **dailyStats:DailyStatistics**
  - Stores aggregated daily biometric data
  - Methods:
    - `+getTodaysReadings(workerId: String, startTime: long) : List<HeartRateReading>`
    - `+addReading(reading: HeartRateReading) : void`

#### External System (Stereotype: <<External>>)
- **healthServices:HealthServices**
  - WearOS HealthServices API
  - Provides passive heart rate monitoring
  - Method: `getLatestMeasurement(dataType: DataType) : DataPoint`

### Key Interaction Flow

1. **User Interaction** (Message 1): TradeWorker glances at watch
2. **View Lifecycle** (Message 2-3): WorkStatusDisplay resumes and requests data refresh
3. **Current BPM Retrieval** (Messages 4-8):
   - HeartRateController requests current heart rate
   - HealthDataRepository queries HealthServices API
   - DataPoint returned with value 125.0 BPM at timestamp 1643970840000
   - Converted to HeartRateReading domain object

4. **Daily Average Calculation** (Messages 9-13):
   - **CRITICAL: StatisticsCalculator.calculateDailyAverage() is called**
   - DailyStatistics provides 247 readings from today
   - **computeAverage() method filters outliers (>200 or <40 BPM)**
   - Returns average: 98.3 BPM

5. **Display Model Creation** (Messages 14-15):
   - HeartRateController creates BpmDisplayModel
   - Status determined as ELEVATED (current > average + 20)
   - Model: {currentBpm: 125, avgBpm: 98, status: ELEVATED}

6. **UI Update** (Messages 16-17):
   - WorkStatusDisplay updates TextView components
   - Color coding applied based on status
   - Visual feedback rendered to user

### Postconditions

#### What the Actor Sees:
1. **Primary display**: Current BPM "125" in large, bold font (32sp)
2. **Secondary display**: "Daily Avg: 98 BPM" in smaller font (18sp)
3. **Status indicator**: Yellow/orange color indicating ELEVATED status
4. **Timestamp**: "Updated 10:34 AM" in small gray text
5. **Visual feedback**: Subtle haptic feedback confirming display update

#### Data State Changes:
1. `healthDataRepo` internal cache updated with latest HeartRateReading object
2. No persistent storage writes (read-only operation for display)
3. `workStatusDisplay.currentModel` updated with new BpmDisplayModel
4. `dailyStats` object maintains in-memory collection (no new data added)
5. View rendering state refreshed in WearOS display buffer

#### System State:
- Background HealthServices monitoring continues
- Next automatic refresh scheduled in 60 seconds
- Battery-efficient passive monitoring remains active
- App lifecycle in RESUMED state

### Design Notes
- Follows strict MVC separation of concerns
- View does not directly access Model
- Controller handles all business logic
- Single Responsibility: Each class has one clear purpose
- StatisticsCalculator is solely responsible for average calculation

---

## Diagram 2: Health & Safety Officer Alert

### Purpose
Models the interaction flow when the Manager Portal (JavaFX application) receives and displays a health alert from a worker's smartwatch via MQTT, notifying the Health & Safety Officer of a significant biometric deviation.

### Preconditions
1. Health & Safety Officer is logged into Manager Portal (JavaFX application)
2. Manager Portal is connected to MQTT broker at `mqtt://alerts.company.com:1883`
3. Officer is subscribed to topic `health/alerts/team/{teamId}`
4. Worker baseline data exists in system (minimum 30 days of resting HR data)
5. Worker's smartwatch has detected anomalous resting heart rate and published alert
6. Officer has Manager Portal window in focus or running in background

### Participants

#### External Actor (Stereotype: <<External>>)
- **mqttBroker:MqttBroker**
  - MQTT message broker (external system)
  - Publishes alerts from worker devices to subscribed clients
  - QoS Level 1 (At least once delivery)

#### Integration Component (Stereotype: <<Integration>>)
- **mqttClient:MqttClient**
  - Eclipse Paho MQTT Java Client wrapper
  - Maintains persistent session with broker
  - Auto-reconnect with exponential backoff
  - Methods:
    - `+connect(brokerUrl: String, clientId: String) : void`
    - `+subscribe(topic: String, qos: int) : void`
    - `+onMessageArrived(topic: String, message: MqttMessage) : void` [callback]
    - `-parseAlertPayload(payload: String) : AlertData`
    - `+publishAck(messageId: int) : void`

#### Controller Components (Stereotype: <<Controller>>)
- **alertController:AlertController**
  - Central coordinator for alert processing
  - Methods:
    - `+handleIncomingAlert(alertData: AlertData) : void`
    - `-createAlertRecord(worker: Worker, alertData: AlertData, analysis: DeviationAnalysis) : HealthAlert`
    - `+acknowledgeAlert(alertId: String, officerId: String) : void`
    - `+getDetailedHistory(workerId: String) : List<BiometricReading>`

- **baselineCalculator:BaselineCalculator**
  - Statistical analysis of biometric deviations
  - **KEY RESPONSIBILITY: Validates if deviation is significant**
  - Methods:
    - `+validateDeviation(workerId: String, currentValue: double, alertType: AlertType) : DeviationAnalysis`
    - `-calculateBaseline(readings: List<BiometricReading>) : BaselineMetrics`
    - `-assessDeviation(currentValue: double, baseline: BaselineMetrics) : DeviationAnalysis`

#### Model Component (Stereotype: <<Model>>)
- **workerHealthModel:WorkerHealthModel**
  - Data access layer for worker health records
  - Database persistence
  - Methods:
    - `+getWorkerById(workerId: String) : Worker`
    - `+getRestingHrHistory(workerId: String, days: int) : List<BiometricReading>`
    - `+saveAlert(alert: HealthAlert) : void`
    - `-persistToDatabase(alert: HealthAlert) : void`
    - `+updateAlertStatus(alertId: String, status: AlertStatus) : void`
    - `+getBiometricHistory(workerId: String, days: int) : List<BiometricReading>`

#### View Components (Stereotype: <<View>>) - JavaFX
- **alertView:AlertView**
  - Main alert display controller (FXML)
  - Manages TableView and modal dialogs
  - Methods:
    - `+displayAlert(alert: HealthAlert) : void` [@FXML]
    - `-updateAlertList(alert: HealthAlert) : void`
    - `-playAlertSound(severity: Severity) : void`
    - `+clickViewDetails(alert: HealthAlert) : void` [@FXML]
    - `-openDetailDialog(worker: Worker, historyData: List<BiometricReading>) : void`

- **alertNotification:AlertNotificationPanel**
  - Animated notification banner
  - Urgency-based styling
  - Methods:
    - `+showNotification(alert: HealthAlert) : void`
    - `-buildNotificationContent(alert: HealthAlert) : VBox`
    - `-applyUrgencyStyle(severity: Severity) : void`
    - `-slideIn(duration: double) : void`
    - `+clickAcknowledge() : void` [@FXML]
    - `-fadeOut() : void`

#### Actor (Stereotype: <<actor>>)
- **HealthSafetyOfficer**
  - End user viewing and responding to alerts

### MQTT Integration Details

#### Subscribed Topic Pattern:
```
health/alerts/team/+
```
- Wildcard `+` allows monitoring all teams
- Examples: `health/alerts/team/engineering`, `health/alerts/team/construction`

#### Message Payload Format (JSON):
```json
{
  "workerId": "W12345",
  "workerName": "John Doe",
  "alertType": "RESTING_HR_DEVIATION",
  "biometricType": "RESTING_HEART_RATE",
  "currentValue": 78.0,
  "baselineValue": 58.2,
  "percentageDeviation": 34.5,
  "timestamp": 1643970840000,
  "severity": "SIGNIFICANT"
}
```

#### QoS Configuration:
- **Quality of Service Level 1**: At least once delivery
- Client sends PUBACK after processing
- Broker will re-deliver if acknowledgment not received
- Prevents message loss during network interruptions

### Key Interaction Flow

1. **MQTT Message Arrival** (Messages 1-3):
   - Broker publishes message to subscribed topic
   - MqttClient callback `onMessageArrived()` triggered
   - JSON payload parsed into AlertData object

2. **Worker Lookup** (Messages 4-6):
   - AlertController retrieves worker details
   - Returns Worker object: {id: 'W12345', name: 'John Doe', team: 'engineering'}

3. **Baseline Validation** (Messages 7-12):
   - **CRITICAL: BaselineCalculator validates the deviation**
   - Fetches 30-day history (420 readings)
   - **calculateBaseline() computes statistics:**
     - Mean = 58.2 BPM
     - Standard Deviation = 4.1 BPM
     - Threshold = 66.4 BPM (mean + 2×stdDev)
   - **assessDeviation() determines:**
     - Current 78 BPM vs Threshold 66.4 BPM
     - Severity: SIGNIFICANT
     - Percentage: 34.5% above baseline

4. **Alert Persistence** (Messages 13-16):
   - HealthAlert record created
   - Saved to HEALTH_ALERTS database table
   - Status: UNACKNOWLEDGED
   - Includes alert_id, timestamps, deviation metrics

5. **UI Notification** (Messages 17-24):
   - **Runs on JavaFX Application Thread** (Platform.runLater)
   - AlertNotificationPanel builds VBox with:
     - Warning icon (⚠)
     - Worker name
     - Deviation details
   - Red border and urgent styling applied
   - 400ms slide-in animation from right edge
   - Alert added to TableView (ObservableList)
   - Urgent.wav sound played

6. **MQTT Acknowledgment** (Message 27):
   - QoS 1 PUBACK sent to broker
   - Message delivery confirmed
   - No re-delivery will occur

7. **Officer Response** (Messages 28+):
   - Visual notification displayed
   - Audio alert played
   - Officer can acknowledge or view details

### Postconditions

#### What the Actor Sees:

1. **Primary Alert Banner** (top-right of screen):
   - Red urgent border with warning icon ⚠
   - Worker name: "John Doe"
   - Alert message: "Resting HR elevated 34.5% above baseline"
   - Metrics: "Current: 78 BPM | Baseline: 58 BPM"
   - Timestamp: "2 minutes ago"
   - Two buttons: [Acknowledge] [View Details]

2. **Alert Table Update**:
   - New row added to alerts TableView
   - Status column shows "UNACKNOWLEDGED" in red
   - Severity column shows "SIGNIFICANT" with urgent icon

3. **Audio Feedback**:
   - Urgent alert tone played once (if sound enabled)

4. **System Tray** (if minimized):
   - Badge count incremented
   - Desktop notification shown

#### Data State Changes:

1. **Database (HEALTH_ALERTS table)** - New record inserted:
   - `alert_id`: "ALT-20260202-103442-001"
   - `worker_id`: "W12345"
   - `alert_type`: "RESTING_HR_DEVIATION"
   - `current_value`: 78.0
   - `baseline_value`: 58.2
   - `deviation_percent`: 34.5
   - `severity`: "SIGNIFICANT"
   - `status`: "UNACKNOWLEDGED"
   - `timestamp`: 1643970840000
   - `acknowledged_by`: NULL
   - `acknowledged_at`: NULL

2. **In-Memory Model Objects**:
   - `alertView.alertList` (ObservableList) has new HealthAlert object
   - `workerHealthModel.activeAlerts` Map updated with alert
   - `alertController.unacknowledgedCount` incremented by 1

3. **UI State**:
   - AlertNotificationPanel visibility = true
   - AlertNotificationPanel opacity animating 0.0 → 1.0
   - Alert table scroll position moved to show new row
   - Badge counter on alerts tab incremented

4. **MQTT State**:
   - Message acknowledged to broker (QoS 1 complete)
   - Client maintains connection for future messages
   - No re-delivery will occur

#### System State:
- Manager Portal remains subscribed to MQTT topics
- Alert persisted for audit trail and reporting
- Officer can take action (acknowledge, view details, contact worker)
- System ready to receive additional alerts
- Background baseline calculations continue for all monitored workers

### Design Notes
- Strict MVC pattern with JavaFX best practices
- Controller manages business logic, never directly updates UI
- View updates always on JavaFX Application Thread
- Model handles all data persistence
- MQTT client provides clean integration layer
- Observer pattern (ObservableList) for reactive UI updates
- Event-driven architecture via MQTT publish/subscribe

---

## Common Design Patterns Used

### Model-View-Controller (MVC)
Both diagrams strictly adhere to MVC separation:
- **Models**: Manage data and business state (no UI knowledge)
- **Views**: Handle UI rendering and user interaction (no business logic)
- **Controllers**: Orchestrate flow between Model and View

### Observer Pattern
- JavaFX ObservableList for reactive UI updates
- MQTT publish/subscribe for event distribution

### Repository Pattern
- HealthDataRepository and WorkerHealthModel abstract data access
- Clean separation from business logic

### Strategy Pattern
- Different alert severity levels trigger different UI behaviors
- Baseline calculation algorithms can be swapped

---

## Technology Stack

### Diagram 1 (WearOS App):
- **Platform**: WearOS 4
- **Device**: Ticwatch E3
- **Language**: Java/Kotlin
- **API**: Android HealthServices API
- **UI Framework**: Jetpack Compose for Wear OS

### Diagram 2 (Manager Portal):
- **Platform**: Desktop (Windows/macOS/Linux)
- **Language**: Java
- **UI Framework**: JavaFX
- **Integration**: Eclipse Paho MQTT Client
- **Database**: SQL (specific RDBMS not specified)
- **Protocol**: MQTT over TCP

---

## Import Instructions for Enterprise Architect

1. Open Enterprise Architect
2. Select **Project → Import Package → Import XMI**
3. Browse to `wearos_health_monitoring.xml`
4. Select package import options:
   - ✓ Import diagrams
   - ✓ Import elements
   - ✓ Import stereotypes
5. Click **Import**
6. Navigate to Project Browser → Packages → "WearOS Health Monitoring System"
7. Open sequence diagrams:
   - "Trade Worker BPM Display"
   - "Health Safety Officer Alert"

### Expected Diagram Structure:
Each diagram will contain:
- Properly stereotyped participants (<<View>>, <<Controller>>, <<Model>>, <<External>>)
- Numbered message sequences
- Activation bars on lifelines
- Return messages (dashed arrows)
- Notes with implementation details
- Self-calls for internal processing

---

## Future Enhancements

### Diagram 1:
- Add error handling flows (sensor disconnected, permission denied)
- Include background sync sequence
- Model notification to user when BPM exceeds safe threshold

### Diagram 2:
- Add alternative flows (acknowledge, view details, dismiss)
- Include batch alert processing
- Model escalation to emergency contacts for critical alerts
- Add reconnection logic for MQTT disconnection scenarios

---

## References

### WearOS Documentation:
- Health Services API: https://developer.android.com/training/wearables/health-services
- Jetpack Compose for Wear: https://developer.android.com/jetpack/compose/wear

### MQTT Resources:
- Eclipse Paho: https://www.eclipse.org/paho/
- MQTT Protocol Specification: https://mqtt.org/mqtt-specification/
- QoS Levels: https://www.hivemq.com/blog/mqtt-essentials-part-6-mqtt-quality-of-service-levels/

### JavaFX:
- JavaFX Documentation: https://openjfx.io/
- FXML Guide: https://docs.oracle.com/javafx/2/fxml_get_started/jfxpub-fxml_get_started.htm

---

## Version History

- **v1.0** (2026-02-02): Initial sequence diagrams created
  - Trade Worker BPM Display
  - Health & Safety Officer Alert
  - Full MVC implementation
  - MQTT integration documented

---

## Contact & Feedback

For questions about these diagrams or the WearOS Health Monitoring System design:
- Review with instructor during lab hours
- Peer feedback sessions
- Submit via course management system

**Remember**: There is no single "correct" design. These diagrams represent one valid approach following MVC principles and best practices.

package com.android.main;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.content.ContextCompat;

import android.os.Bundle;
import android.util.Log;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import org.eclipse.paho.client.mqttv3.*;
import org.eclipse.paho.android.service.*;


public class MainActivity extends AppCompatActivity {
    private final String broker = "tcp://192.168.18.173:1883";
    private final String username = "mbkm";
    private final String password = "mbkm";
    private final String clientId = "Subscribe : Gamzv (Java)";
    private final String topic = "device/room/kitchen/";
    private final int qos = 0;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Button btnConnect = findViewById(R.id.btnConnect);
        Button btnDisconnect = findViewById(R.id.btnDisconnect);
        EditText temp = findViewById(R.id.etTemp);
        EditText humidity = findViewById(R.id.etHumd);

        temp.setEnabled(false);
        temp.setTextColor(ContextCompat.getColor(this, R.color.white));
        humidity.setEnabled(false);
        humidity.setTextColor(ContextCompat.getColor(this, R.color.white));
        btnConnect.setEnabled(true);
        btnDisconnect.setEnabled(false);


        MqttConnectOptions options = new MqttConnectOptions();
        options.setUserName(username);
        options.setPassword(password.toCharArray());

        MqttAndroidClient client = new MqttAndroidClient(this, broker, clientId);

        btnConnect.setOnClickListener(v -> {
            try {
                client.connect(options, null, new IMqttActionListener() {
                    @Override
                    public void onSuccess(IMqttToken asyncActionToken) {
                        Toast.makeText(MainActivity.this, "Connected to Broker", Toast.LENGTH_LONG).show();
                        btnDisconnect.setEnabled(true);
                        btnConnect.setEnabled(false);
                        Subscribe(client, topic, qos, temp, humidity);
                    }

                    @Override
                    public void onFailure(IMqttToken asyncActionToken, Throwable exception) {
                        Toast.makeText(MainActivity.this, exception.getMessage(), Toast.LENGTH_LONG).show();
                    }
                });
            } catch (MqttException e) {
                Log.d("connection-error", e.getMessage());
            }
        });

        btnDisconnect.setOnClickListener(v -> {
            try {
                client.unsubscribe(topic);
                client.disconnect(null, new IMqttActionListener() {
                    @Override
                    public void onSuccess(IMqttToken asyncActionToken) {
                        Toast.makeText(MainActivity.this, "Disconnected from broker", Toast.LENGTH_LONG).show();
                        btnDisconnect.setEnabled(false);
                        btnConnect.setEnabled(true);
                        temp.setText("0");
                        humidity.setText("0");
                    }

                    @Override
                    public void onFailure(IMqttToken asyncActionToken, Throwable exception) {
                        Toast.makeText(MainActivity.this, exception.getMessage(), Toast.LENGTH_LONG).show();
                    }
                });
            } catch (MqttException e) {
                e.printStackTrace();
            }
        });
    }

    private void Subscribe(MqttAndroidClient client, String topic, int qos, EditText temprature, EditText humidity) {
        try {
            client.subscribe(topic, qos);
            client.setCallback(new MqttCallback() {
                @Override
                public void connectionLost(Throwable cause) {
                    
                }

                @Override
                public void messageArrived(String topic, MqttMessage message) throws Exception {
                    String[] msg = new String(message.getPayload()).split(":");
                    temprature.setText(msg[0]);
                    humidity.setText(msg[1]);
                    Log.d("message-sub", "messageArrived: " + msg[0] + ":" + msg[1]);
                }

                @Override
                public void deliveryComplete(IMqttDeliveryToken token) {

                }
            });
        } catch (MqttException e) {
            Log.d("subscribe-err", "subscribe err: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
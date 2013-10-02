using UnityEngine;
using System.Collections;
using System.Net.Sockets;
using System.IO;
using System.Linq;
using System;

public class CortexClient {
	private TcpClient tcpClient;
	private NetworkStream stream;
	private StreamReader reader;
	
	public CortexClient(string host, int port) {
		try {
			tcpClient = new TcpClient (host, port);
		} catch (SocketException) {
			IsOnline = false;
			return;	
		}

		IsOnline = true;
		stream = tcpClient.GetStream ();
		reader = new StreamReader (stream);
	}
	
	public bool IsOnline { get; private set; }
	public bool HasDataz { get { return IsOnline && stream.DataAvailable; } }
	
	public int[] GetDataz() {
		if (HasDataz) {
			var data = reader.ReadLine();
			return data.Split(',').Select(s => Convert.ToInt32(s)).ToArray();
		}
		return null;
	}
}

public class NetworkClient : MonoBehaviour
{
	private CortexClient cc;
	
	// Use this for initialization
	void Start ()
	{
		cc = new CortexClient("localhost", 1337);
	}
	
	// Update is called once per frame
	void Update ()
	{
		int[] dataz = cc.GetDataz();
		if (dataz == null) {
			return; // No data
		}
		
		var sphere = GetComponent<MeshRenderer>();
		float v = (float)dataz[0] / 5000.0f - 1.0f;
		sphere.material.color = new Color(v * v, 0.2f, 0.5f * v);
			
		var t = GetComponent<Transform>();
		t.localScale = new Vector3(v * 70f, v* 70f, v* 70f);	
	}
}

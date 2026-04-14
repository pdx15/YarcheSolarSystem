using UnityEngine;
using System.IO;
using System.Collections.Generic;

[System.Serializable]
public class BodyData
{
    public float x;
    public float y;
    public float z;
}

public class SolarSystemLoader : MonoBehaviour
{
    public string filePath = "unity_positions.json";
    public GameObject planetPrefab;

    private Dictionary<string, GameObject> bodies = new();

    void Start()
    {
        Load();
    }

    void Load()
    {
        string json = File.ReadAllText(Application.dataPath + "/" + filePath);

        var dict = JsonUtility.FromJson<Wrapper>(json);

        foreach (var kv in dict.data)
        {
            GameObject obj = Instantiate(planetPrefab);
            obj.name = kv.Key;

            var cb = obj.AddComponent<CelestialBody>();
            cb.bodyName = kv.Key;

            cb.SetPosition(new Vector3(kv.Value.x, kv.Value.y, kv.Value.z));

            bodies[kv.Key] = obj;
        }
    }

    [System.Serializable]
    class Wrapper
    {
        public Dictionary<string, BodyData> data;
    }
}
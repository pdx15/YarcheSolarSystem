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

    public float positionScale = 1e-7f;
    public float distanceMultiplier = 50f;

    private Dictionary<string, GameObject> bodies = new();

    void Start()
    {
        Load();
    }

	void Load()
	{
		string fullPath = Path.Combine(Application.dataPath, filePath);

		if (!File.Exists(fullPath))
		{
			Debug.LogError("Файл не найден: " + fullPath);
			return;
		}

		string json = File.ReadAllText(fullPath);
		JsonData dict = JsonUtility.FromJson<JsonData>(json);

		if (dict == null || dict.keys == null)
		{
			Debug.LogError("Ошибка чтения JSON");
			return;
		}

		// 1. НАЙТИ ЦЕНТР (СОЛНЦЕ / СРЕДНЕЕ)
		Vector3 center = Vector3.zero;

		for (int i = 0; i < dict.values.Length; i++)
		{
			center += new Vector3(
				dict.values[i].x,
				dict.values[i].y,
				dict.values[i].z
			);
		}

		center /= dict.values.Length;

		// 2. МАСШТАБ (ВАЖНО)
		float scale = 1e-8f; // 👈 вот это ключ

		for (int i = 0; i < dict.keys.Length; i++)
		{
			string key = dict.keys[i];
			BodyData val = dict.values[i];

			GameObject obj = Instantiate(planetPrefab);
			obj.name = key;

			obj.transform.localScale = Vector3.one * 0.5f;

			Vector3 rawPos = new Vector3(val.x, val.y, val.z);

			// центрируем систему + масштабируем
			Vector3 pos = (rawPos - center) * scale;

			obj.transform.position = pos;

			var cb = obj.AddComponent<CelestialBody>();
			cb.bodyName = key;

			ApplyTexture(obj, key);

			bodies[key] = obj;

			Debug.Log("Создано: " + key + " at " + pos);
		}

		Debug.Log("Solar System loaded: " + dict.keys.Length);
	}

    void ApplyTexture(GameObject obj, string name)
    {
        string cleanName = name.Replace(" BARYCENTER", "").Replace(" ", "");
        string path = "Textures/" + cleanName.ToLower();

        Texture tex = Resources.Load<Texture>(path);

        if (tex != null)
        {
            var renderer = obj.GetComponent<Renderer>();

            renderer.material = new Material(renderer.material);
            renderer.material.mainTexture = tex;

            renderer.material.EnableKeyword("_EMISSION");
            renderer.material.SetColor("_EmissionColor", Color.white * 0.8f);
            renderer.material.SetTexture("_EmissionMap", tex);
        }
        else
        {
            Debug.LogWarning("Нет текстуры: " + name + " (ищем: " + path + ")");
        }
    }

    [System.Serializable]
    public class JsonData
    {
        public string[] keys;
        public BodyData[] values;
    }
}
using UnityEngine;

public class CelestialBody : MonoBehaviour
{
    public string bodyName;
    public string spiceName;

    public float distanceScale = 1f;

    public void SetPosition(Vector3 pos)
    {
        transform.position = pos * distanceScale;
    }
}